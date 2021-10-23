from backend.models import Post, Inbox
from rest_framework import viewsets, permissions 
from .serializers import PostSerializer, InboxSerializer

# Viewset for Post
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PostSerializer


# Viewset for Inbox
class InboxViewSet(viewsets.ModelViewSet):
    '''
    Specifies a view for a list of items in inbox 
    '''

    # Check permissions to require access to data
    permission_classes = [
        permissions.AllowAny
    ]
    # Serializer used to return a JSON response
    serializer_class = InboxSerializer

    queryset = Inbox.objects.all()
