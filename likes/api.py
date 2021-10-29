from rest_framework.generics import get_object_or_404
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

import uuid
import ast

class PostLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_post_likes(self, request, author_id, post_id):
        query_set = Like.objects.filter(post=Post.objects.get(id=post_id))
        response = LikeSerializer(query_set, many=True).data
        
        for likeObj in response:
            likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
            likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
            name = likeObj['author']["displayName"]
            likeObj["summary"] = f"{name} Likes your post"
            likeObj["object"] = request.build_absolute_uri().strip("/likes")
            
        return Response(response, status=status.HTTP_200_OK)
        
    def add_post_like(self, request, author_id, post_id):
        author_inst = Author.objects.get(user = request.user)
        
        try:
            query_set = Post.objects.get(id=post_id).like_set.create(author=author_inst)
        except:
            return Response({"message": "You have already liked the post!"}, status=status.HTTP_403_FORBIDDEN)
        
        response = LikeSerializer(query_set).data

        response['@context'] = "https://www.w3.org/ns/activitystreams"
        response['author'] = AuthorSerializer(Author.objects.get(id=response["author"])).data
        name = response['author']["displayName"]
        response["summary"] = f"{name} Likes your post"
        response["object"] = request.build_absolute_uri().strip("/likes")
            
        return Response(response, status=status.HTTP_200_OK)
        
        
class CommentLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    
    def get_comment_likes(self, request, author_id, post_id, comment_id):
        query_set = Like.objects.filter(comment=Comment.objects.get(id=comment_id))
        response = LikeSerializer(query_set, many=True).data
        
        for likeObj in response:
            likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
            likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
            name = likeObj['author']["displayName"]
            likeObj["summary"] = f"{name} Likes your comment"
            likeObj["object"] = request.build_absolute_uri().strip("/likes")
            
        return Response(response, status=status.HTTP_200_OK)
        
    def add_comment_like(self, request, author_id, post_id, comment_id):
        author_inst = Author.objects.get(user = request.user)
        
        try:
            query_set = Comment.objects.get(id=comment_id).like_set.create(author=author_inst)
        except:
            return Response({"message": "You have already liked the comment!"}, status=status.HTTP_403_FORBIDDEN)
        
        response = LikeSerializer(query_set).data

        response['@context'] = "https://www.w3.org/ns/activitystreams"
        response['author'] = AuthorSerializer(Author.objects.get(id=response["author"])).data
        name = response['author']["displayName"]
        response["summary"] = f"{name} Likes your comment"
        response["object"] = request.build_absolute_uri().strip("/likes")
            
        return Response(response, status=status.HTTP_200_OK)
