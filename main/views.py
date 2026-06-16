from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, ProfileForm, PortfolioImageForm
from .models import Profile, PortfolioImage, ChatRoom, Message
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    return render(request, 'main/home.html')

def register(request):
    role_pref = request.GET.get('role', '')
    if request.method == 'POST':
        uform = UserRegisterForm(request.POST)
        pform = ProfileForm(request.POST, request.FILES)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            user.set_password(uform.cleaned_data['password'])
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            if profile.role == 'instructor':
                return redirect('main:dashboard_instructor')
            else:
                return redirect('main:dashboard_learner')
    else:
        uform = UserRegisterForm()
        pform = ProfileForm(initial={'role': role_pref})
    return render(request, 'main/register.html', {'uform': uform, 'pform': pform})

def user_login(request):
    role_pref = request.GET.get('role','')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=username, password=pwd)
        if user:
            login(request, user)
            if user.profile.role == 'instructor':
                return redirect('main:dashboard_instructor')
            else:
                return redirect('main:dashboard_learner')
        else:
            error = 'Invalid credentials'
    return render(request, 'main/login.html', {'error': error, 'role_pref': role_pref})

def user_logout(request):
    logout(request)
    return redirect('main:home')

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.role == 'instructor':
        portfolio = profile.portfolio.all()
        pform = ProfileForm(instance=profile)
        pif = PortfolioImageForm()
        chat_rooms = ChatRoom.objects.filter(instructor=profile)
        return render(request, 'main/dashboard_instructor.html', {'profile': profile, 'portfolio': portfolio, 'pform': pform, 'pif': pif, 'chat_rooms': chat_rooms})
    else:
        pform = ProfileForm(instance=profile)
        chat_rooms = ChatRoom.objects.filter(learner=profile)
        return render(request, 'main/dashboard_learner.html', {'profile': profile, 'pform': pform, 'chat_rooms': chat_rooms})

def instructor_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk, role='instructor')
    portfolio = profile.portfolio.all()
    return render(request, 'main/instructor_profile.html', {'profile': profile, 'portfolio': portfolio})

def search_page(request):
    return render(request, 'main/search.html')

def api_search_instructors(request):
    q = request.GET.get('q','').strip()
    results = Profile.objects.filter(role='instructor')
    if q:
        results = results.filter(Q(domain__icontains=q) | Q(name__icontains=q) | Q(user__username__icontains=q))
    data = []
    for p in results:
        data.append({
            'id': p.id,
            'username': p.user.username,
            'name': p.name,
            'domain': p.domain,
            'bio': p.bio,
            'photo_url': p.photo.url if p.photo else ''
        })
    return JsonResponse({'results': data})

@login_required
def api_upload_portfolio(request):
    profile = request.user.profile
    if profile.role != 'instructor':
        return JsonResponse({'error': 'Only instructors can upload'}, status=403)
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        pi = PortfolioImage.objects.create(profile=profile, image=img)
        return JsonResponse({'ok': True, 'image_url': pi.image.url})
    return JsonResponse({'error': 'No file'}, status=400)

@login_required
def chat(request, user_id):
    other_user_profile = get_object_or_404(Profile, pk=user_id)
    my_profile = request.user.profile

    print(f"DEBUG: My Profile ID: {my_profile.id}, Role: {my_profile.role}")
    print(f"DEBUG: Other User Profile ID: {other_user_profile.id}, Role: {other_user_profile.role}")

    if my_profile.role == 'learner' and other_user_profile.role == 'instructor':
        learner = my_profile
        instructor = other_user_profile
    elif my_profile.role == 'instructor' and other_user_profile.role == 'learner':
        learner = other_user_profile
        instructor = my_profile
    else:
        # Handle cases where two instructors or two learners try to chat
        chat_error = "You cannot chat with users of the same role."
        return render(request, 'main/chat.html', {
            'chat_error': chat_error,
            'other_user': other_user_profile
        })

    # Get or create chat room
    chat_room, created = ChatRoom.objects.get_or_create(
        learner=learner,
        instructor=instructor
    )

    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            Message.objects.create(
                chat_room=chat_room,
                sender=my_profile,
                content=content
            )
        return redirect('main:chat', user_id=user_id)

    messages = chat_room.messages.order_by('timestamp')
    return render(request, 'main/chat.html', {
        'chat_room': chat_room,
        'messages': messages,
        'other_user': other_user_profile
    })

@login_required
def video_call(request, user_id):
    other_user_profile = get_object_or_404(Profile, pk=user_id)
    return render(request, 'main/video_call.html', {'other_user': other_user_profile})

@csrf_exempt
def api_chatbot(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_message = data.get('message', '').lower().strip()

        # Rule-based responses for login/register help and general assistance
        responses = {
            'login': "To log in, go to the login page and enter your username and password. If you forgot your password, contact support.",
            'register': "To register, click on 'Register' in the top navigation. Choose your role (Learner or Instructor) and fill in the required details.",
            'help': "I'm here to help! You can ask me about login, registration, or general platform features.",
            'instructor': "Instructors can create profiles, upload portfolios, and connect with learners for teaching opportunities.",
            'learner': "Learners can search for instructors, view their profiles, and start chats or video calls.",
            'search': "Use the search page to find instructors by domain or name. You can then view their profiles and contact them.",
            'chat': "You can chat with instructors or learners through the chat feature on their profiles.",
            'video': "Video calls are available for direct communication with instructors or learners.",
            'profile': "Update your profile information from your dashboard to showcase your skills and experience.",
            'portfolio': "Instructors can upload portfolio images to demonstrate their work and expertise.",
        }

        # Check for keywords in user message
        response = "I'm sorry, I didn't understand that. Try asking about login, register, or platform features."
        for key, resp in responses.items():
            if key in user_message:
                response = resp
                break

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)
