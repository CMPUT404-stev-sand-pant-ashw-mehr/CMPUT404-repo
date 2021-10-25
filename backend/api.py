from backend.models import Post 
from rest_framework import viewsets, permissions, pagination
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = PostSerializer
    
    pagination_class = pagination.PageNumberPagination

    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return self.request.user.posts.all()
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    @action(detail=True, methods=['GET', 'POST'], name='comments')
    def comments(self, request, pk=None):
        if(request.method == 'GET'):
            query_set = Post.objects.get(id=pk).comment_set.all()
            page = self.paginate_queryset(query_set)
            response = CommentSerializer(page, many=True)
            return self.get_paginated_response(response.data)
            
        elif(request.method =='POST'):
            Post.objects.get(id=pk).comment_set.create(author=request.user, comment=request.data["comment"])
            return Response({
                "message": "Comment Added"
            })