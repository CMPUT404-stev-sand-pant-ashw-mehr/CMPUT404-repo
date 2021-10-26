from django.urls import path, re_path
from followers.api import FollowerViewSet

urlpatterns = [
    path('author/<str:author_id>/followers/', FollowerViewSet.as_view({"get": "list"})),
    re_path(r'^author/(?P<author_id>\w+)/followers/(?P<foreign_author_id>\w+)/?$', FollowerViewSet.as_view({
        "get": "check_follower", 
        "put": "put_follower", 
        "delete": "delete_follower"
        })), # Using re_path because APPEND_SLASH doesn't work with put
]