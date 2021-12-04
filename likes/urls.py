from django.urls import re_path

from .api import PostLikeViewSet, CommentLikeViewSet, AuthorLikeViewSet

urlpatterns = [
    re_path(r'^author/(?P<author_id>[a-z0-9-\.-]+)/post/(?P<post_id>[a-z0-9-:\.-]+)/likes/?$', PostLikeViewSet.as_view({
            "get": "get_post_likes", 
            "post": "add_post_like",
            })),
    re_path(r'^author/(?P<author_id>[a-z0-9-/:\.-]+)/post/(?P<post_id>[a-z0-9-:\.-]+)/comments/(?P<comment_id>[a-z0-9-:\.-]+)/likes/?$', CommentLikeViewSet.as_view({
            "get": "get_comment_likes", 
            "post": "add_comment_like",
            })),
    re_path(r'^author/(?P<author_id>[a-z0-9-\.-]+)/likes/?$', AuthorLikeViewSet.as_view({
            "get": "get_likes", 
            })),
    re_path(r'^author/(?P<author_id>(http://|https://)[a-z0-9\.-:]+(/author/)[a-z0-9\.-]+)/likes/?$', AuthorLikeViewSet.as_view({
            "get": "get_likes", 
            }))
]