from author.models import Author
from comment.models import Comment
from likes.models import Like
from post.models import Post
from rest_framework import viewsets, status
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LikeSerializer
from author.serializer import AuthorSerializer
from accounts.permissions import CustomAuthentication, AccessPermission
from accounts.helper import is_valid_node
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json

class PostLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomAuthentication,)
    permission_classes = (AccessPermission,)
    serializer_class = LikeSerializer
        
    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/post/< POST_ID >/likes",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "summary": "Lara Croft Likes your post",         
                        "type": "Like",
                        "author":{
                            "type":"author",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Lara Croft",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github":"http://github.com/laracroft",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        },
                        "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
                    }
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
        },
        tags=['Get Post Likes'],
    )
    def get_post_likes(self, request, author_id, post_id):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

        query_set = Like.objects.filter(post=Post.objects.get(id=post_id))
        response = LikeSerializer(query_set, many=True).data
        
        for likeObj in response:
            likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
            likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
            name = likeObj['author']["displayName"]
            
        return Response(response, status=status.HTTP_200_OK)
        
    
    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/post/< POST_ID >/likes",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "summary": "Lara Croft Likes your post",         
                        "type": "Like",
                        "author":{
                            "type":"author",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Lara Croft",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github":"http://github.com/laracroft",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        },
                        "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
                    }
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
            "409": openapi.Response(
                description="Conflict",
                examples={
                    "application/json":{"message": "error"}
                }
            ),
        },
        tags=['Like Post'],
    )
    def add_post_like(self, request, author_id, post_id):
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

        result, obj = add_author_to_database(request=request)
        if not result:
            return Response(obj, status=status.HTTP_400_BAD_REQUEST)
        else:
            author_inst = obj

        try:
            query_set = Post.objects.get(id=post_id).like_set.create(author=author_inst, object=request.build_absolute_uri().strip("/likes"))
        except Exception as e:
            return Response({"message": e.args}, status=status.HTTP_409_CONFLICT)
        
        response = LikeSerializer(query_set).data

        response['@context'] = "https://www.w3.org/ns/activitystreams"
        response['author'] = AuthorSerializer(Author.objects.get(id=response["author"])).data
        name = response['author']["displayName"]
        response["summary"] = f"{name} Likes your post"
            
        return Response(response, status=status.HTTP_200_OK)
        
        
class CommentLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomAuthentication,)
    permission_classes = (AccessPermission,)
    serializer_class = LikeSerializer
    
    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/post/< POST_ID >/comments/{ COMMENT_ID }/likes",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "summary": "Lara Croft Likes your comment",         
                        "type": "Like",
                        "author":{
                            "type":"author",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Lara Croft",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github":"http://github.com/laracroft",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        },
                        "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e/comments/764efa883dda1e11db47671c4a3bbd9f"
                    }
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
        },
        tags=['Get Comment Likes'],
    )
    def get_comment_likes(self, request, author_id, post_id, comment_id):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
            
        query_set = Like.objects.filter(comment=Comment.objects.get(id=comment_id))
        response = LikeSerializer(query_set, many=True).data
        
        for likeObj in response:
            likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
            likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
            name = likeObj['author']["displayName"]
            likeObj["summary"] = f"{name} Likes your comment"
            
        return Response(response, status=status.HTTP_200_OK)
        
        
    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/post/< POST_ID >/comments/{ COMMENT_ID }/likes",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "summary": "Lara Croft Likes your comment",         
                        "type": "Like",
                        "author":{
                            "type":"author",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Lara Croft",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github":"http://github.com/laracroft",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        },
                        "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e/comments/764efa883dda1e11db47671c4a3bbd9f"
                    }
                }
            ),
            "403": openapi.Response(
                description="Forbidden",
                examples={
                    "application/json":{"message":"Node not allowed"}
                }
            ),
            "409": openapi.Response(
                description="Conflict",
                examples={
                    "application/json":{"message": "error"}
                }
            ),
        },
        tags=['Like Comment'],
    )
    def add_comment_like(self, request, author_id, post_id, comment_id):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            Post.objects.get(id=post_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        result, obj = add_author_to_database(request=request)
        if not result:
            return Response(obj, status=status.HTTP_400_BAD_REQUEST)
        else:
            author_inst = obj
        
        try:
            query_set = Comment.objects.get(id=comment_id).like_set.create(author=author_inst, object=request.build_absolute_uri().strip("/likes"))
        except Exception as e:
            return Response({"message": e.args}, status=status.HTTP_409_CONFLICT)
        
        response = LikeSerializer(query_set).data

        response['@context'] = "https://www.w3.org/ns/activitystreams"
        response['author'] = AuthorSerializer(Author.objects.get(id=response["author"])).data
        name = response['author']["displayName"]
        response["summary"] = f"{name} Likes your comment"
        response["object"] = request.build_absolute_uri().strip("/likes")
            
        return Response(response, status=status.HTTP_200_OK)


class AuthorLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomAuthentication,)
    permission_classes = (AccessPermission,)
    serializer_class = LikeSerializer

    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/liked",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "type":"liked",
                    "items":[
                        {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "summary": "Lara Croft Likes your post",         
                            "type": "Like",
                            "author":{
                                "type":"author",
                                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                "host":"http://127.0.0.1:5454/",
                                "displayName":"Lara Croft",
                                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                "github":"http://github.com/laracroft",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                            },
                            "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
                        }
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
                    "application/json":{"detail": "author not found"}
                }
            ),
        },
        tags=['Get Comment Likes'],
    )
    def get_likes(self, request, author_id):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        if not Author.objects.exclude(is_active=False).filter(id=author_id).exists():
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
            
        query_set = Like.objects.filter(author=author_id).all()
        data = LikeSerializer(query_set, many=True).data
        
        for likeObj in data:
            likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
            likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
            name = likeObj['author']["displayName"]

            objUrlsplitted = likeObj['object'].split('/')
            if {"post", "posts"}.intersection(set(objUrlsplitted)):
                ptype = "post"
            else:
                ptype = "comment"

            likeObj["summary"] = f"{name} Likes your {ptype}"
        
        response = {
            'type': 'liked',
            "items": data
        }
        
        return Response(response, status=status.HTTP_200_OK)


def add_author_to_database(request):
    try:
        author_json = request.POST["author"]
        if type(author_json) == dict:
            author_dict = author_json
        else:
            author_dict = json.loads(author_json)
    except KeyError:
        try:
            author = Author.objects.get(user = request.user)
            return True, author
        except:
            return False, {"detail": "JSON author missing"}
    except json.JSONDecodeError as e:
        return False, {"detail": f"Invalid author JSON: {e.msg}"}

    author_validation = AuthorSerializer(data=author_dict)
    if not author_validation.is_valid():
        return False, author_validation.error_messages
    else:
        author, created = Author.objects.get_or_create(id = author_dict["id"])
        author_dict.pop("id")

        if not created:
            author_dict.pop("url")
            author_dict.pop("host")

        for key, value in author_dict.items():
            try:
                setattr(author, key, value)
            except:
                pass

        author.is_active = True
        author.save()
        return True, author
    