from backend.models import Post, Inbox, Author
from rest_framework import viewsets, permissions, pagination, status
from .serializers import PostSerializer, CommentSerializer, InboxSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 

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



class InboxViewSet(viewsets.ModelViewSet):
    '''
    Specifies a view for a list of items in inbox 
    '''

    # Check permissions to require access to data
    permission_classes = [
        permissions.IsAuthenticated
    ]
    # Serializer used to return a JSON response
    serializer_class = InboxSerializer

    queryset = Inbox.objects.all()


    def list(self,request, author_id=None, *args, **kwargs):
        # Check if author exists
        try:
            check_author = Author.objects.filter(id=author_id).get()
        except:
            response = {
                "author": "unknown",
                "items": {}
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
            
