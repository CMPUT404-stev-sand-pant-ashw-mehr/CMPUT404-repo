from author.models import Author
from post.models import Post
from rest_framework import status, viewsets, permissions, pagination
from .serializers import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 

from django.forms.models import model_to_dict

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_post_comments(self, request, author_id=None, post_id=None):
        try:
            author_query = Author.objects.exclude(user__isnull=True).get(id=author_id)
            post_query = Post.objects.get(id=post_id, author=author_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        author_detail = model_to_dict(author_query)

        # replace the id field (used internally) to the url
        author_detail['id'] = author_detail['url']

        # remove the 'user' column, used internally for linking User model
        author_detail.pop('user', None)

    def add_comment_to_post(self, request, author_id=None, post_id=None):
        pass
