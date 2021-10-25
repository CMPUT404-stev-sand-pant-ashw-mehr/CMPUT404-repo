from django.urls import path
from followers.api import FollowerViewSet

urlpatterns = [
    path('author/<str:author_id>/followers/', FollowerViewSet.as_view({"get": "list"})),
    path('author/<str:author_id>/followers/<str:foreign_author_id>/', FollowerViewSet.as_view({
        "get": "check_follower", 
        "put": "put_follower", 
        "delete": "delete_follower"
        })),
    path('author/<str:author_id>/followers/<str:foreign_author_id>', FollowerViewSet.as_view({"put": "put_follower"})) #append slash doesn't work with put so a URL with no slash is needed
]