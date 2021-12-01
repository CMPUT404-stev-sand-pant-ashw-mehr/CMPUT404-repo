from django.urls import path, include

from .api import LoginAPI, ProfileAPI, RegisterAPI, get_foregin_authors_view, get_foregin_author_detail_view, get_foregin_posts_view, get_foregin_post_detail_view
from knox import views as knox_views 

urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/profile', ProfileAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view()),
    path('connection/authors', get_foregin_authors_view),
    path('connection/posts', get_foregin_posts_view),
    path('connection/author-detail/<str:author_id>', get_foregin_author_detail_view),
    path('connection/post-detail/<str:post_id>', get_foregin_post_detail_view)
]