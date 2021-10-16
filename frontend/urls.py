from django.urls import path 
from frontend.views import Index 

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('feed', Index.as_view(), name='feed'),
]