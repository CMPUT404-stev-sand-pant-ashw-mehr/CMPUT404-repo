from django.urls import path, include, re_path

from .api import LoginAPI, ProfileAPI, RegisterAPI, get_foregin_authors_view, get_foregin_author_detail_view, get_foregin_posts_view, get_foregin_post_detail_view, github_view, send_friend_request, like_foregin_post, comment_foregin_post, view_comment_foreign_post
from knox import views as knox_views 

urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/profile', ProfileAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view()),
    path('connection/comments', view_comment_foreign_post),
    path('connection/authors', get_foregin_authors_view),
    path('connection/posts', get_foregin_posts_view),
    path('connection/author-detail/<str:author_id>', get_foregin_author_detail_view),
    path('connection/post-detail/<str:post_id>', get_foregin_post_detail_view),
    path('connection/<str:author_id>/like/<str:post_id>', like_foregin_post),
    path('connection/<str:author_id>/comment/<str:post_id>/<str:content>', comment_foregin_post),
    re_path(r'^connection/friend-request/(?P<local_author_id>[a-z0-9\.-]+)/(?P<foreign_author_id>(http://|https://)[a-z0-9\.-:]+(/author/)[a-z0-9\.-]+)/?$',send_friend_request),
    re_path(r'^connection/friend-request/(?P<local_author_id>[a-z0-9\.-]+)/(?P<foreign_author_id>[a-z0-9\.-]+)/?$',send_friend_request),
    path('author/<str:author_id>/github',github_view),
    
]