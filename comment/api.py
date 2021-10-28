from post.models import Post 
from rest_framework import viewsets, permissions, pagination
from .serializers import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_post_comments(self, request, author_id=None, post_id=None):
        pass

    def add_comment_to_post(self, request, author_id=None, post_id=None):
        pass
    