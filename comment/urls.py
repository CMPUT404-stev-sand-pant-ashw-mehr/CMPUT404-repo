from django.urls import path, re_path

from .api import CommentViewSet

urlpatterns = [
    re_path(r'^author/(?P<author_id>[a-z0-9-/:\.-]+)/posts/(?P<post_id>[a-z0-9-/:\.-]+)/comments/?$', CommentViewSet.as_view({
        "get": "get_post_comments", 
        "post": "add_comment_to_post"
        }))
]
