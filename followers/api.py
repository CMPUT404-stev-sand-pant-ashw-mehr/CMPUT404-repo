from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from Project.social_distribution.author.models import Author
from Project.social_distribution.author.serializer import AuthorSerializer
from followers.models import Followers
from .serializers import FollowerSerializer
from django.contrib.auth.models import User
import requests

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    # GET list of followers
    def list(self, request, author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        follower_rows = Followers.objects.filter(author_id=author_id).values()
        # check if follower_rows is empty
        if not len(follower_rows):
            return Response({
                "type": "followers",
                "items":{}
            })
        
        follower_items = list()

        for follower in follower_rows:
            follower_details = requests.get(follower["follower_url"])
            if follower_details.status_code == 200:
                serializer = AuthorSerializer(follower_details.text)
                if serializer.is_valid():
                    follower_items.append(serializer.data)
                else:
                    print(serializer.errors)

        return Response({
                "type": "followers",
                "items": str(follower_items)
            })


    