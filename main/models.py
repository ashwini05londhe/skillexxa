from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('instructor','Instructor'),
        ('learner','Learner')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')

    name = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=32, blank=True)

    profession = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=200, blank=True)
    domain = models.CharField(max_length=100, blank=True)

    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class PortfolioImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolio')
    image = models.ImageField(upload_to='portfolio/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username}"


class ChatRoom(models.Model):
    learner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chat_rooms_as_learner')
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chat_rooms_as_instructor')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('learner', 'instructor')

    def __str__(self):
        return f"Chat between {self.learner.user.username} and {self.instructor.user.username}"


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user.username} at {self.timestamp}"
