from django.urls import include, re_path

from .api import PostViewSet

urlpatterns = [
     re_path(r'^author/(?P<author_id>\w+)/posts/?$', PostViewSet.as_view({
         "get": "get_recent_post", 
         "post": "create_post"
         })),
     re_path(r'^author/(?P<author_id>\w+)/posts/(?P<post_id>\w+)/?$', PostViewSet.as_view({
         "get": "get_post", 
         "post": "update_post", 
         "delete": "delete_post", 
         "put": "create_post"
         }))
]