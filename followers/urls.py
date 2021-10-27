from django.urls import path, re_path
from followers.api import FollowerViewSet

urlpatterns = [
    path('author/<str:author_id>/followers/', FollowerViewSet.as_view({"get": "list"})),
    re_path(r'^author/(?P<author_id>[a-z0-9/:\.]+)/followers/(?P<foreign_author_id>[a-z0-9/:\.]+)/?$', FollowerViewSet.as_view({
        "get": "check_follower", 
        "put": "put_follower", 
        "delete": "delete_follower"
        })), # Using re_path because APPEND_SLASH doesn't work with put
        # Example URL: http://127.0.0.1:8000/author/3aowe9uvgsao/followers/http://anthoerhost.com/author/f09sdg0bv0as9dfg
        #                                          { author_id }         {               foreign_author_id               }
]
