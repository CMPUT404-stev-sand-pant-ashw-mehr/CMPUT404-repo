from django.forms.models import model_to_dict
from rest_framework.generics import get_object_or_404
from author.models import Author
from comment.models import Comment
from comment.serializers import CommentSerializer
from post.models import Post 
from rest_framework import viewsets, pagination, status
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_post(self, request, author_id=None, post_id=None):
        try:
            # get post with author.
            post_query = Post.objects.get(id=post_id, author=author_id)

            # get author. Exclude foreign author
            author_query = Author.objects.exclude(user__isnull=True).get(id=author_id)

        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        post_data = PostSerializer(data=post_query).data
        author_detail = model_to_dict(author_query)
        author_detail['id'] = author_detail['url']

        post_data['id'] = author_detail['id'] + '/posts/' + post_data['id']
        post_data['author'] = author_detail
        post_data['comments'] = post_data['id'] + '/comments'

        try:
            comment_query = Comment.objects.get(post=post_id, author=author_id)
            comment_details = model_to_dict(comment_query)
        except:
            post_data["count"] = 0
            post_data["CommentsSrc"] = {}

        return Response(post_data, status=status.HTTP_200_OK)

    def get_recent_post(self, request, author_id=None):
        pass

    def update_post(self, request, author_id=None, post_id=None):
        pass

    def create_post(self, request, author_id=None, post_id=None):
        pass

    def delete_post(self, request, author_id=None, post_id=None):
        pass
    