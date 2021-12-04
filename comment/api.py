from re import I
import uuid
from comment.models import Comment
from author.models import Author
from author.serializer import AuthorSerializer
from post.models import Post
from rest_framework import status, viewsets
from .serializers import CommentSerializer
from rest_framework.response import Response 
from django.core.paginator import Paginator

from django.forms.models import model_to_dict

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.permissions import AccessPermission, CustomAuthentication
from accounts.helper import is_valid_node

import uuid
import json

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    
    def initialize_request(self, request, *args, **kwargs):
     self.action = self.action_map.get(request.method.lower())
     return super().initialize_request(request, *args, kwargs)
    
    def get_authenticators(self):
        if self.action in ["get_post_comments", ]:
            return [CustomAuthentication()]
        else:
            return [TokenAuthentication()]
    
    def get_permissions(self):
        if self.action in ["get_post_comments",]:
            return [AccessPermission()]
        else:
            return [IsAuthenticated()]


    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/posts/< POST_ID >/comments",
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
                    "application/json":{
                        "type":"comments",
                        "page":1,
                        "size":5,
                        "post":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                        "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                        "comments":[
                            {
                                "type":"comment",
                                "author":{
                                    "type":"author",
                                    "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                    "host":"http://127.0.0.1:5454/",
                                    "displayName":"Greg Johnson",
                                    "github": "http://github.com/gjohnson",
                                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                },
                                "comment":"Sick Olde English",
                                "contentType":"text/markdown",
                                "published":"2015-03-09T13:07:04+00:00",
                                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                            }
                        ]
                    }
                }
                
            ),
            "400": openapi.Response(
                description="Bad Request"
            ),
            "404": openapi.Response(
                description="Post not found",
                examples={
                    "application/json":{"detail": "post not found"}
                }
            )
        },
        tags=['Get Comments on a Post'],
    )
    def get_post_comments(self, request, author_id=None, post_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]

        try:
            author = Author.objects.exclude(is_active=False).exclude(user__isnull=True).get(id=author_id)
            Post.objects.get(id=post_id, author_id=author_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        page = request.GET.get('page', 'None')
        size = request.GET.get('size', 'None')

        query = Comment.objects.filter(author=author_id)

        if(page == "None" or size == "None"):
            comment_query = query.values()
        else:
            paginator = Paginator(query.values(), size)
            comment_query = paginator.get_page(page).object_list

        return_list = list()
        for comment in comment_query:
            comment_author_id = comment.pop('author_id', None)
            author_details = model_to_dict(Author.objects.get(id=comment_author_id))
            author_details['id'] = author_details['url']
            comment['author'] = author_details
            comment["id"] = author_details["url"] + '/posts/' + post_id + '/comments/' + comment['id']
            return_list.append(comment)
        
        return Response({
            "type": "comments",
            "page": page,
            "size": size,
            "post": str(request.build_absolute_uri()).replace("/comments", ''),
            "id": str(request.build_absolute_uri()),
            "comments": return_list
        }, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/posts/< POST_ID >/comments",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["type", "author", "comment", "contentType", "published", "id"],
            properties={
                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                    "author": openapi.Schema(type=openapi.TYPE_OBJECT),
                    "comment": openapi.Schema(type=openapi.TYPE_STRING),
                    "contentType": openapi.Schema(type=openapi.TYPE_STRING),
                    "published": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "id": openapi.Schema(type=openapi.TYPE_STRING)
                },
        ),
        responses={
            "201": openapi.Response(
                description="Created",
                examples={
                    "application/json":{
                        'id': 'http://testserver/author/897sdga89s7df89a/posts/9bf46de854ab44d183848b02c9ae86cd/comments/fbcbee22ba024290bddb44948b0de7d1', 
                        'published': '2021-12-04T09:02:59.281452Z', 
                        'type': 'comment', 
                        'author': {
                            'id': 'http://127.0.0.1:8000/author/897sdga89s7df89a', 
                            'host': 'http://127.0.0.1:8000/', 
                            'url': 'http://127.0.0.1:8000/author/897sdga89s7df89a', 
                            'displayName': 'NewName', 
                            'github': 'https://github.com/testUser1', 
                            'profileImage': 'None'
                        }, 
                        'post_id': 'http://testserver/author/897sdga89s7df89a/posts/9bf46de854ab44d183848b02c9ae86cd', 
                        'comment': 'This is a test comment', 
                        'contentType': 'text/plain'
                    }
                }
            ),
            "403": openapi.Response(
                description="Forbidden"
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json":{"detail": "author not found"},
                    "application/json":{"detail": "post not found"},
                    "application/json":{"detail": "Missing fields", "message": "Error details..."}
                }
            ),
        },
        tags=['Add Comments to a Post'],
    )
    # POST to add new comment
    def add_comment_to_post(self, request, author_id=None, post_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]
        
        try:
            Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            Post.objects.get(id=post_id, author=author_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            author_json = request.data["author"]
            if type(author_json) == dict:
                author_dict = author_json
            else:
                author_dict = json.loads(author_json)
        except KeyError:
            return Response({"detail": "JSON author missing"}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            return Response({"detail": f"Invalid author JSON: {e.msg}"}, status=status.HTTP_400_BAD_REQUEST)

        author_validation = AuthorSerializer(data=author_dict)
        if not author_validation.is_valid():
            return Response(author_validation.error_messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            author, _ = Author.objects.get_or_create(author_dict["id"])
            author_dict.pop("id")
            for key, value in author_dict.items():
                try:
                    setattr(author, key, value)
                except:
                    pass
            author.save()

        try:
            comment_id = uuid.uuid4().hex
            keys = {
                "id": comment_id,
                "type": request.data["type"],
                "author": author,
                "post_id": post_id,
                "comment": request.data["comment"],
                "contentType": request.data["contentType"]
            }
            comment = Comment.objects.create(**keys)
            comment.save()
            keys["author"] = author_validation.data
            keys.pop("id")
            keys.pop("post_id")
            return Response({
                "id": request.build_absolute_uri() + '/' + comment_id,
                "published": comment.published,
                "post": request.build_absolute_uri().split("/comments")[0],
                **keys,
            }, status=status.HTTP_201_CREATED)
      
        except KeyError as e:
            return Response({"detail": "Missing fields", "message": e.args}, status=status.HTTP_400_BAD_REQUEST)
