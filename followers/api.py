from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from followers.models import Followers
from .serializers import FollowerSerializer
from django.contrib.auth.models import User

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def list(self, request, author_id=None):
        get_object_or_404(User, pk=author_id)
        serializer = self.get_serializer()

        return Response({
            "type": "followers",
            "items":[serializer.data]
        })

    