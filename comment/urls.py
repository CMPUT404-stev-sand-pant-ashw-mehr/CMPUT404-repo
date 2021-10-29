from django.urls import path, re_path

from .api import CommentViewSet

urlpatterns = [
    re_path(r'^author/(?P<author_id>\w+)/posts/(?P<post_id>\w+)/comments/?$', CommentViewSet.as_view({
        "get": "get_post_comments", 
        "post": "add_comment_to_post"
        }))
]
