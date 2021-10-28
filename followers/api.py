from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from followers.serializers import FollowerModelSerializer
from author.serializer import AuthorSerializer
from author.models import Author
from followers.models import Followers
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from urllib.parse import urlparse

import io
from rest_framework.parsers import JSONParser

class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET list of followers
    def list(self, request, author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        follower_rows = Followers.objects.filter(author=author_id).values()
        # check if follower_rows is empty
        if not len(follower_rows):
            return Response({
                "type": "followers",
                "items":[{}]
            }, status=status.HTTP_200_OK)
        follower_items = list()

        # Get the updated information for each followers
        for follower in follower_rows:
            follower_id = follower["follower_id"] # Django will add "_id" suffix for all Foreign key field and there is no trivial way of overriding that

            # Remove potential trailing slash of the follower id. 
            if follower_id[-1] == '/':
                follower_id = follower_id[:-1]

            follower_details = Author.objects.filter(id=follower_id).values()[0]
            follower_details['id'] = follower_details['url']
            follower_items.append(follower_details)

        return Response({
                "type": "followers",
                "items": follower_items
            }, status=status.HTTP_200_OK)

    # PUT a follower to the specified author
    def put_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        # Remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]

        try:
            content_type = request.META["CONTENT_TYPE"]

            if content_type != "application/json":
                return Response({"detail": "invalid content type. Required: application/json"}, status=status.HTTP_400_BAD_REQUEST)

            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)

            # Remove trailing slashes of the url
            try:
                id_url = data["id"]
                
                if not self.validate_url(id_url):
                    return Response({"detail": "follower id format invalid"}, status=status.HTTP_400_BAD_REQUEST)

                # Remove trailing slash
                if id_url[-1] == '/':
                    data["id"] = id_url[:-1]
            except KeyError:
                return Response({"detail": "id Field of PUT data missing"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AuthorSerializer(data=data)

            if serializer.is_valid():
                # validate if the id in request body matches the foreign_author_id
                request_body = serializer.validated_data
                follower_url = str(request_body["url"])

                if not self.validate_url(follower_url):
                    return Response({"detail": "follower url format invalid"}, status=status.HTTP_400_BAD_REQUEST)

                # Remove trailing slash
                if follower_url[-1] == '/':
                    follower_url = follower_url[:-1]
            
                if follower_url != foreign_author_id.strip():
                    return Response({"detail": "author id in URL does not match id in PUT body"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Save author to database via serializer
                    serializer.save()
            else:
                return Response({"detail": "Invalid json for author", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "PUT missing body with content_type: application/json"}, status=status.HTTP_400_BAD_REQUEST)

        # Store to Follower Database
        data = dict()
        data["author"] = author_id
        data["follower"] = foreign_author_id.strip()
        serializer = FollowerModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "error when storing to database", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE a follower of a given author
    def delete_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        # remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]

        if not Followers.objects.filter(follower=foreign_author_id).exists():
            return Response({"detail": "follower not found"}, status=status.HTTP_404_NOT_FOUND)
        
        Followers.objects.filter(follower=foreign_author_id).delete()

        return Response(status=status.HTTP_200_OK)

    # GET if the author has the follower with the given id on the server
    def check_follower(self, request, author_id=None, foreign_author_id=None):
        
        get_object_or_404(User, pk=author_id) # Check if user exists

        # remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]
            
        if Followers.objects.filter(author=author_id, follower=foreign_author_id).exists():
            return Response({"detail": True}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": False}, status=status.HTTP_404_NOT_FOUND)

    # validate if the url format is correct
    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

