from django.urls import path, include 
from .api import LoginAPI, ProfileAPI, RegisterAPI
from knox import views as knox_views 

urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/profile', ProfileAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view())
]