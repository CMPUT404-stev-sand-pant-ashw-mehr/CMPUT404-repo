from django.urls import path, include 
from .api import LoginAPI, ProfileAPI, RegisterAPI, get_foregin_authors, get_foregin_posts
from knox import views as knox_views 

urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/profile', ProfileAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view()),
    path('connection/authors', get_foregin_authors),
    path('connection/posts', get_foregin_posts)
]