from django.urls import re_path

from .api import PostLikeViewSet, CommentLikeViewSet

urlpatterns = [
    re_path(r'^author/(?P<author_id>[a-z0-9-/:\.-]+)/posts/(?P<post_id>[a-z0-9-:\.-]+)/likes/?$', PostLikeViewSet.as_view({
            "get": "get_post_likes", 
            "post": "add_post_like",
            })),
    re_path(r'^author/(?P<author_id>[a-z0-9-/:\.-]+)/posts/(?P<post_id>[a-z0-9-:\.-]+)/comments/(?P<comment_id>[a-z0-9-:\.-]+)/likes/?$', CommentLikeViewSet.as_view({
            "get": "get_comment_likes", 
            "post": "add_comment_like",
            }))
]