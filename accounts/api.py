from rest_framework import generics, permissions, status, validators
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response 
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from author.serializer import AuthorSerializer
from django.contrib.auth.models import User
from author.models import Author
from .helper import get_list_foregin_authors, get_list_foregin_posts, is_valid_node, get_foregin_author_detail, get_foregin_public_post_detail, send_friend_request_helper, like_foreign_posts, comment_foreign_posts, view_comments_foreign_post
from author.models import Author
from .permissions import AccessPermission, CustomAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid, requests
import json


class RegisterAPI(generics.GenericAPIView):
    """
    User & Author Registration
    """
    serializer_class = RegisterSerializer
    
    @swagger_auto_schema(
        operation_description="POST /auth/register/",
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "displayName": openapi.Schema(type=openapi.TYPE_STRING),
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "github": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":{
                        "user": {
                            "id": 1,
                            "username": "abc",
                            "author": "b0463cf2aabe4ef88e9332aa018142e5"
                        }
                    }
                }
                
            ),
            "400": openapi.Response(
                description="Bad Reequest",
                examples={
                    "application/json":{
                        "username": [
                            "A user with that username already exists."
                        ]
                    }
                }
                
            )
        },
        tags=['Login'],
    )
    def post(self, request):
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        if request.is_secure():
            host = 'https://' + str(request.get_host())
        else:
            host = 'http://' + str(request.get_host())

        user_serializer = self.get_serializer(data = request.data)
        user_serializer.is_valid(raise_exception=True)
        # create user
        user = user_serializer.save()

        author_uuid = uuid.uuid4().hex

        author_schema = {
            "host" : host,
            "id": str(author_uuid),
            "user_id": user.id,
            "url": host + '/author/' + str(author_uuid),
            "displayName": request.data["displayName"],
            "github": request.data["github"],
            "is_active": False  # Not approved when created
        }

        Author.objects.create(**author_schema)

        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    '''
    Takes username & password to autheticate the user
    '''
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="POST /auth/register/",
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "displayName": openapi.Schema(type=openapi.TYPE_STRING),
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "github": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":{
                        "user": {
                            "id": 1,
                            "username": "abc",
                            "author": "90d16d62804347cb806cb9812f617a7f"
                        },
                        "author": {
                            "id": "http://127.0.0.1:8000/author/90d16d62804347cb806cb9812f617a7f",
                            "type": "author",
                            "host": "http://127.0.0.1:8000",
                            "url": "http://127.0.0.1:8000/author/90d16d62804347cb806cb9812f617a7f",
                            "displayName": "abc",
                            "github": "abc@github.com",
                            "profileImage": ""
                        },
                        "token": "cfcf3c9aa1f4858e8de8502762a7d3aea4727e16b1585a67c4ca1d3e0ad35178"
                    }
                }
                
            ),
            "400": openapi.Response(
                description="Bad Reequest",
                examples={
                    "application/json":{
                        "non_field_errors": [
                            "Incorrect username or password."
                        ]
                    }
                }
            ),
            "401": openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json":{
                        "message": "Unauthorized User"
                    }
                }
            )
        },
        tags=['Register'],
    )
    def post(self, request, *args, **kwargs):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.select_related('author').get(username=username)
        try:
            get_object_or_404(Author, id=user.author.id, is_active=True)
        except:
            return Response({
                "message": "Unauthorized User"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'user': UserSerializer(user).data,
            'author': AuthorSerializer(user.author).data,
            'token': AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)


class ProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user

    def retrieve(self, request):
        return Response({
            'user': UserSerializer(self.get_queryset()).data,
            'author': AuthorSerializer(User.objects.select_related('author').get(username=request.user.username).author).data
        }, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_description="GET /connection/authors",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"foregin authors": []}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Get all foreign authors'],
)
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_authors_view(request):
    if request.method == "GET":
        foreign_authors = get_list_foregin_authors()
        print(foreign_authors)
        return Response({"items": foreign_authors})
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@swagger_auto_schema(
    method='get',
    operation_description="GET /connection/posts",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"items": []}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Get all foreign posts'],
)
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_posts_view(request):
    if request.method == "GET":
        foreign_posts = get_list_foregin_posts()
        print(foreign_posts)
        return Response({"items": foreign_posts})
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
'''
get foreign author/post detail
'''
@swagger_auto_schema(
    method='get',
    operation_description="GET connection/author-detail/<str:author_id>",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"items": []}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                   "application/json": {"detail": "can't find this author"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Get all foreign author details'],
)
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_author_detail_view(request, author_id):
    if request.method == "GET":
        
        foreign_author = get_foregin_author_detail(author_id)
        if foreign_author != "author not found!":
            return Response({"items": foreign_author}) 
        else:
            return Response({"detail": "can't find this author"}, status=status.HTTP_404_NOT_FOUND) 
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@swagger_auto_schema(
    method='get',
    operation_description="GET connection/post-detail/<str:post_id>",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"items": []}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                   "application/json": {"detail": "can't find this post"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Get all foreign post details'],
)
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_post_detail_view(request, post_id):
    if request.method == "GET":
        post = get_foregin_public_post_detail(post_id)
        if post != "post not found!":
            return Response({"items": post}) 
        else:
            return Response({"detail": "can't find this post"}, status=status.HTTP_404_NOT_FOUND) 
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

'''
get author's github activities
'''   
@swagger_auto_schema(
    method='get',
    operation_description="GET author/<str:author_id>/github",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": "view"}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                   "application/json": {"detail": "github not provided!"},
                   "application/json": {"detail": "github not found!"}
                }
            )
    },
    tags=['Github View'],
)
@api_view([ 'GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def github_view(request, author_id):
    # get github activity
    if request.method == "GET":
        author = get_object_or_404(Author,id = author_id)
        username = author.github
        if username == None:
            return Response({"detail": "github not provided!"}, status=status.HTTP_404_NOT_FOUND)
        git_username = username.split(".")[-1].split("/")[-1]
        url = 'https://api.github.com/users/'+ git_username + '/events'
        git_msg = requests.get(url, headers={'Referer': "https://social-dis.herokuapp.com/"}).json()
        if type(git_msg) != list:
            return Response({"detail": "github not found!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(git_msg, status=status.HTTP_200_OK)

'''
send friend request to other teams
'''       
@swagger_auto_schema(
    method='post',
    operation_description="POST connection/friend-request/<str:local_author_id>/<str:foreign_author_id>",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"message": "incoming response text"}
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                   "application/json": {"detail": "incoming response"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Send Friend Request'],
)
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def send_friend_request(request, local_author_id, foreign_author_id):
    if request.method == "POST":
        request_response = send_friend_request_helper(local_author_id, foreign_author_id)
        if type(request_response) == str:
            return Response({"detail": request_response}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": request_response.text}, status=request_response.status_code)
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
'''
comment & like foreign posts
'''    
@swagger_auto_schema(
    method='post',
    operation_description="POST connection/<str:author_id>/like/<str:post_id>",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": f"author has already liked a foreign post"},
                   "application/json": {"detail": f"author liked a foreign post"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Like Foreign Posts'],
)
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def like_foregin_post(request, post_id, author_id):
    author = Author.objects.get(id=author_id)
    if request.method == "POST":
        res = like_foreign_posts(post_id, author)
        if res.text ==  '{"succ":false}':
            return Response({"detail": f"{author.displayName} has already liked a foreign post"}, status=status.HTTP_200_OK)
        return Response({"detail": f"{author.displayName} liked a foreign post"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@swagger_auto_schema(
    method='post',
    operation_description="POST connection/<str:author_id>/comment/<str:post_id>/<str:content>",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": f"author has already commented on a foreign post"},
                   "application/json": {"detail": f"author commented a foreign post"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['Comment Foreign Posts'],
)
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def comment_foregin_post(request, post_id, author_id, content):
    author = Author.objects.get(id=author_id)
    if request.method == "POST":
        res = comment_foreign_posts(post_id, author, content)
        if res.text ==  '{"succ":false}':
            return Response({"detail": f"{author.displayName} has already commented a foreign post"}, status=status.HTTP_200_OK)
        return Response({"detail": f"{author.displayName} commented on a foreign post"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='post',
    operation_description="POST connection/comments",
    responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": "incoming response"}
                }
            ),
            "405": openapi.Response(
                description="Method Not Allowed",
                examples={
                   "application/json": {"message": "Method Not Allowed"}
                }
            )
    },
    tags=['View Comment Foreign Posts'],
)
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def view_comment_foreign_post(request):
    commentsUrl = request.data['commentsUrl']

    if request.method == "POST":
        res = view_comments_foreign_post(commentsUrl)
        return Response(res, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)