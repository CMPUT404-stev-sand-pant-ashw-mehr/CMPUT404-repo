from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from followers.serializers import FollowerModelSerializer
from author.serializer import AuthorSerializer
from followers.models import Followers
from django.contrib.auth.models import User

import io
from rest_framework.parsers import JSONParser

import requests

class FollowerViewSet(viewsets.ModelViewSet):

    # GET list of followers
    def list(self, request, author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists
        follower_rows = Followers.objects.filter(author_id=author_id).values()
        # check if follower_rows is empty
        if not len(follower_rows):
            return Response({
                "type": "followers",
                "items":[{}]
            }, status=status.HTTP_200_OK)
        follower_items = list()

        # Get the updated information for each followers
        for follower in follower_rows:
            f_url = str(follower["follower_url"])

            # Get follower details via url
            try:
                follower_details = requests.get(f_url)
            except:
                continue

            if follower_details.status_code == 200:
                serializer = AuthorSerializer(data=follower_details.json())
                if serializer.is_valid():
                    follower_items.append(serializer.data)
                else:
                    print(serializer.errors)

        return Response({
                "type": "followers",
                "items": str(follower_items)
            }, status=status.HTTP_200_OK)

    def put_follower(self, request, author_id=None, foreign_author_id=None):
        # check if user is authorized:
        if not request.user.is_authenticated:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        get_object_or_404(User, pk=author_id) # Check if user exists

        try:
            content_type = request.META["CONTENT_TYPE"]

            if content_type != "application/json":
                raise Response({"detail": "invalid content type. Required: application/json"}, status=status.HTTP_400_BAD_REQUEST)

            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            serializer = AuthorSerializer(data=data)

            if not serializer.is_valid():
                return Response({"detail": "Invalid json format for author", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"detail": "PUT missing body with content_type: application/json"}, status=status.HTTP_400_BAD_REQUEST)

        request_body = serializer.validated_data
        follower_url = str(request_body["url"])

        # Validate the follower id matches the id supplied in url
        follower_id = follower_url.split("followers/")[-1].strip()
        
        if follower_id != foreign_author_id.strip():
            return Response({"detail": "author id in URL does not match id in PUT body"}, status=status.HTTP_400_BAD_REQUEST)

        data = dict()
        data["author_id"] = author_id
        data["follower_url"] = follower_url
        serializer = FollowerModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "error when storing to database", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        

    def delete_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

    def check_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists
