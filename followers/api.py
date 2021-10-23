from rest_framework import viewsets
from rest_framework.response import Response
from followers.models import Followers
from .serializers import FollowerSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def list(self, request, author_id=None):
        serializer = self.get_serializer()
        return Response({
            "type": "followers",
            "items":[serializer.data]
        })
