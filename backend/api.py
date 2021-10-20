from backend.models import Post, Comment
from rest_framework import viewsets, permissions 
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Viewset for Post
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = PostSerializer
    
    def get_queryset(self):
        return self.request.user.posts.all()
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    
#Viewset for Comments
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    
    @action(detail=True, methods=['GET', 'POST'], name='comments')
    def comments(self, request, pk=None):
        if(request.method == 'GET'):
            query_set = Post.objects.get(id=pk).comment_set.all()
            response = CommentSerializer(query_set, many=True)
            return Response(response.data)
            
        elif(request.method =='POST'):
            Post.objects.get(id=pk).comment_set.create(author=request.user, comment=request.data["comment"])
            return Response({
                "message": "Comment Added"
            })
        
