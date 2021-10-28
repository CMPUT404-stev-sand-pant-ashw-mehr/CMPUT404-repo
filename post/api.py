from post.models import Post 
from rest_framework import viewsets, permissions, pagination
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_post(self, request, author_id=None, post_id=None):
        pass

    def get_recent_post(self, request, author_id=None):
        pass

    def update_post(self, request, author_id=None, post_id=None):
        pass

    def create_post(self, request, author_id=None, post_id=None):
        pass

    def delete_post(self, request, author_id=None, post_id=None):
        pass
    