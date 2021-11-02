from rest_framework import response
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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import io
from rest_framework.parsers import JSONParser

class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/followers",
        manual_parameters=[
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="optional", 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'size', 
                openapi.IN_QUERY, 
                description="optional", 
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                        {
                            
                            "type": "followers",      
                            "items":[
                                {
                                    "type":"author",
                                    "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                    "host":"http://127.0.0.1:5454/",
                                    "displayName":"Greg Johnson",
                                    "github": "http://github.com/gjohnson",
                                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                },
                                {
                                    "type":"author",
                                    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                    "host":"http://127.0.0.1:5454/",
                                    "displayName":"Lara Croft",
                                    "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                    "github": "http://github.com/laracroft",
                                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                }
                            ]
                        }
                }
            )
        },
        tags=['Get all Followers'],
    )

    # GET list of followers
    def list(self, request, author_id=None):
        get_object_or_404(Author, pk=author_id) # Check if user exists

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


    @swagger_auto_schema(
        operation_description="PUT /service/author/< AUTHOR_ID >/followers/< FOREIGN_AUTHOR_ID >",
        responses={
            "201": openapi.Response(
                description="Created",
            ),
            "400": openapi.Response(
                description="Bad request",
                examples={
                    "application/json":{"detail": "invalid content type. Required: application/json"},
                    "application/json":{"detail": "follower id format invalid"},
                    "application/json":{"detail": "id Field of PUT data missing"},
                    "application/json":{"detail": "follower url format invalid"},
                    "application/json":{"detail": "author id in URL does not match id in PUT body"},
                    "application/json":{"detail": "Invalid json for author", "errors": "Error details"},
                    "application/json":{"detail": "error when storing to database", "error": "Error details"},
                    "application/json":{"detail": "PUT missing body with content_type: application/json"}
                }
            ),

        },
        tags=['Add a Follower to an Author'],
    )

    # PUT a follower to the specified author
    def put_follower(self, request, author_id=None, foreign_author_id=None):
        # check user
        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

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



    @swagger_auto_schema(
        operation_description="DELETE /service/author/< AUTHOR_ID >/followers/< FOREIGN_AUTHOR_ID >",
        responses={
            "200": openapi.Response(
                description="OK"
            ),
            "404": openapi.Response(
                description="Follower not found",
                examples={
                    "application/json":{"detail": "follower not found"}
                }
            ),
        },
        tags=['Delete a Follower'],
    )
    # DELETE a follower of a given author
    def delete_follower(self, request, author_id=None, foreign_author_id=None):
        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]

        if not Followers.objects.filter(follower=foreign_author_id).exists():
            return Response({"detail": "follower not found"}, status=status.HTTP_404_NOT_FOUND)
        
        Followers.objects.filter(follower=foreign_author_id).delete()

        return Response(status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/followers/< FOREIGN_AUTHOR_ID >",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": True}
                }
            ),
            "404": openapi.Response(
                description="Follower not found",
                examples={
                    "application/json":{"detail": False}
                }
            ),
        },
        tags=['Check if Follower'],
    )
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

