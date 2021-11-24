from django.urls import include, re_path, path
from .api import PostViewSet
from .api import get_posts as get_public_posts

urlpatterns = [
    re_path(r'^author/(?P<author_id>[a-z0-9-:\.-]+)/posts/?$', PostViewSet.as_view({
         "get": "get_recent_post", 
         "post": "create_post"
         })),
    re_path(r'^author/(?P<author_id>[a-z0-9-/:\.-]+)/posts/(?P<post_id>[a-z0-9-:\.-]+)/?$', PostViewSet.as_view({
         "get": "get_post", 
         "post": "update_post", 
         "delete": "delete_post", 
         "put": "create_post"
         })),
    path("posts/", PostViewSet.as_view({"get": "get_public_posts"})),
]