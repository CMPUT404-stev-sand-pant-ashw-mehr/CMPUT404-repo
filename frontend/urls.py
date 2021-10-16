from django.urls import path 
from frontend.views import Index 

urlpatterns = [
    path('', Index.as_view(), name='index'),
<<<<<<< HEAD
<<<<<<< HEAD
    path('feed', Index.as_view(), name='feed'),
=======
>>>>>>> 03b29879a368a6a8752038b7ccbe3af6930724d3
=======
>>>>>>> 03b29879a368a6a8752038b7ccbe3af6930724d3
]