from backend.models import Post 
from rest_framework import viewsets, permissions, pagination
from .serializers import PostSerializer 

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = PostSerializer

    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return self.request.user.posts.all()
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)