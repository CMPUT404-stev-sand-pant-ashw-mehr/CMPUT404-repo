from backend.models import Post 
from rest_framework import viewsets, permissions 
from .serializers import PostSerializer 

# Viewset for Post
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = PostSerializer

    def get_queryset(self):
        return self.request.user.posts.all()
        
    #Override
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)