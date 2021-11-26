from rest_framework import response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from accounts.permissions import AccessPermission, CustomAuthentication
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
from accounts.helper import is_valid_node

import io
from rest_framework.parsers import JSONParser

class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerModelSerializer

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, kwargs)
    
    def get_authenticators(self):
        if self.action in ["list", "check_follower"]:
            return [CustomAuthentication()]
        else:
            return [TokenAuthentication()]
    
    def get_permissions(self):
        if self.action in ["list", "check_follower"]:
            return [AccessPermission()]
        else:
            return [IsAuthenticated()]

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
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json":{"message": "author does not exist"}
                }
            ),
        },
        tags=['Get all Followers'],
    )

    # GET list of followers
    # NEED CONNECTION
    def list(self, request, author_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
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
                examples={
                    "application/json":{
                        "follow": {}, 
                        "follower": {},
                        "object": {},
                        "invalid keys": []
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad request",
                examples={
                    "application/json":[
                        {"detail": "invalid content type. Required: application/json"},
                        {"detail": "follower id format invalid"},
                        {"detail": "id Field of PUT data missing"},
                        {"detail": "follower url format invalid"},
                        {"detail": "author id in URL does not match id in PUT body"},
                        {"detail": "Invalid json for author", "errors": "Error details"},
                        {"detail": "error when storing to database", "error": "Error details"},
                        {"detail": "PUT missing body with content_type: application/json"}
                    ]
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json":{"message": "author does not exist"}
                }
            ),

        },
        tags=['Add a Follower to an Author'],
    )

    # PUT a follower to the specified author
    def put_follower(self, request, author_id=None, foreign_author_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        #check user
        try:
            author = Author.objects.exclude(is_active=False).get(id=author_id)
        except Author.DoesNotExist:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if Followers.objects.filter(author=author_id, follower=foreign_author_id).exists():
            return Response({"detail": "follower already added!"}, status=status.HTTP_409_CONFLICT)
            
        try:
            stream = io.BytesIO(request.body)
            put_data = JSONParser().parse(stream)
        except:
            put_data = dict()

        # remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]
            
        try:
            foreign_author = Author.objects.exclude(is_active=False).get(id=foreign_author_id)
            invalid_keys = list()
            #Update the foreign_author in Author model by given key
            for key in put_data:
                if self.check_author_key(key.strip(), ['displayName', 'github', 'profileImage']):
                    value = put_data[key]
                    setattr(foreign_author, key, value)
                    foreign_author.save()
                else:
                    invalid_keys.append(key)            
            
            newFollow = Followers.objects.create(author=author, follower=foreign_author)

            return Response({
                "follow": FollowerModelSerializer(newFollow).data, 
                "follower": AuthorSerializer(foreign_author).data,
                "object": AuthorSerializer(author).data,
                "invalid keys": invalid_keys
            }, status=status.HTTP_201_CREATED)

        except Author.DoesNotExist:

            if request.META.get('CONTENT_TYPE') != 'application/json':
                return Response({"detail": "PUT missing body with content_type: application/json"}, status=status.HTTP_400_BAD_REQUEST)

            required_fields = {'displayName', 'github', 'profileImage', 'host', 'url'}
            
            if not required_fields.issubset(set(put_data)):
                return Response({"detail": f"Keys missing for put: {required_fields.difference(put_data)}"}, status=status.HTTP_400_BAD_REQUEST)

            newAuthorKeys = {
                "id": foreign_author_id,
                "is_active": True
            }

            invalid_keys = list()
            for key in put_data:
                if self.check_author_key(key.strip(), required_fields):
                    newAuthorKeys[key] = put_data[key]
                else:
                    invalid_keys.append(key)

            newAuthor = Author.objects.create(**newAuthorKeys)

            newFollow = Followers.objects.create(author=author, follower=newAuthor)
            
            return Response({
                "follow": FollowerModelSerializer(newFollow).data, 
                "follower": AuthorSerializer(newAuthor).data,
                "object": AuthorSerializer(author).data,
                "invalid keys": invalid_keys
            }, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_description="DELETE /service/author/< AUTHOR_ID >/followers/< FOREIGN_AUTHOR_ID >",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":{"detail": "follower deleted"}
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
            "404": openapi.Response(
                description="Follower not found",
                examples={
                    "application/json":[
                        {"detail": "follower not found"},
                        {"detail": "author not found"},
                    ]
                }
            ),
        },
        tags=['Delete a Follower']
    )
    # DELETE a follower of a given author
    # NEED CONNECTION
    def delete_follower(self, request, author_id=None, foreign_author_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            author = Author.objects.exclude(is_active=False).get(id=author_id)
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

        return Response({"detail": "follower deleted"}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/followers/< FOREIGN_AUTHOR_ID >",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": [
                        {"detail": True},
                        {"detail": False}
                    ]
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json":{"message": "author does not exist"}
                }
            ),
        },
        tags=['Check if Follower'],
    )
    # GET if the author has the follower with the given id on the server
    # NEED CONNECTION
    def check_follower(self, request, author_id=None, foreign_author_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        get_object_or_404(Author, pk=author_id) # Check if user exists

        # remove trailing slash
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]
            
        if Followers.objects.filter(author=author_id, follower=foreign_author_id).exists():
            return Response({"detail": True}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": False}, status=status.HTTP_200_OK)

    # validate if the url format is correct
    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def check_author_key(self, key, valid_keys):
        # Only these keys are allowed to be changed for Author
        if key in valid_keys:
            return True
        else:
            return False

        
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
@swagger_auto_schema(
        operation_description="GET author/<str:author_id>/friends",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {"type": "friends","items":[]}
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"not a valid node"}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json":{"message": "author does not exist"}
                }
            ),
        },
        tags=['Get Friends'],
    )
def get_friends(request, author_id):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        Author.objects.exclude(is_active=False).filter(id = author_id)
    except Author.DoesNotExist:
        return Response({"message": "author does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    follow = Followers.objects.filter(author_id=author_id)
    serializer = FollowerModelSerializer(follow, many=True)
    
    print(serializer.data)
    followers = []
    friends = []
    
    for author in serializer.data:
        follower_id = author['follower']
        try:
            follower = Author.objects.exclude(is_active=False).get(id=follower_id)
            serializer = AuthorSerializer(follower)
            followers.append(serializer.data)
        except Author.DoesNotExist:
            return Response({"message": "No such follower!"})
        
    for f in followers:
        follower_id = f['id'].split("/")[-1]
        if Followers.objects.filter(follower_id=author_id, author_id=follower_id).exists():
            # check if mutually followed, if ture, friend
            friends.append(f)
            
    return Response({"type": "friends","items":friends}, status=status.HTTP_200_OK)
    
    
    
    
    
    
    
