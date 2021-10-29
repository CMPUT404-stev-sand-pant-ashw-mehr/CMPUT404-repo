from comment.models import Comment
from author.models import Author
from post.models import Post
from rest_framework import status, viewsets
from .serializers import CommentSerializer
from rest_framework.response import Response 
from django.core.paginator import Paginator

from django.forms.models import model_to_dict

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_post_comments(self, request, author_id=None, post_id=None):
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]

        try:
            Author.objects.exclude(user__isnull=True).get(id=author_id)
            Post.objects.get(id=post_id, author=author_id)
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

        serialzer = CommentSerializer(data=comment_query, many=True)

        if serialzer.is_valid():
            return_list = list()
            for comment in serialzer.data:
                author = comment["author"]
                comment["id"] = author["url"] + '/posts/' + post_id + '/comments/' + comment['id']
                return_list.append(comment)
            
            return Response({
                "type": "comments",
                "page": page,
                "size": size,
                "post": str(request.build_absolute_uri()).replace("/comments", ''),
                "id": str(request.build_absolute_uri()),
                "comments": return_list
            }, status=status.HTTP_200_OK)
        else:
            return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


    # POST to add new comment
    def add_comment_to_post(self, request, author_id=None, post_id=None):
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]

        try:
            Author.objects.exclude(user__isnull=True).get(id=author_id)
            Post.objects.get(id=post_id, author=author_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            keys = {
                "type": request.data["type"],
                "author": author_id,
                "post": post_id,
                "comment": request.data["comment"],
                "contentType": request.data["contentType"]
            }
            comment = Comment.objects.create(**keys)
            return Response(comment.save(), status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"detail": "Missing fields", "message": e.args}, status=status.HTTP_400_BAD_REQUEST)
