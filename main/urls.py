from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/instructor/", views.dashboard, name="dashboard_instructor"),
    path("dashboard/learner/", views.dashboard, name="dashboard_learner"),
    path("search/", views.search_page, name="search"),
    path("instructor/<int:pk>/", views.instructor_profile, name="instructor_profile"),
    path("api/search/", views.api_search_instructors, name="api_search"),
    path("api/upload-portfolio/", views.api_upload_portfolio, name="api_upload_portfolio"),
    path("chat/<int:user_id>/", views.chat, name="chat"),
    path("video-call/<int:user_id>/", views.video_call, name="video_call"),
]