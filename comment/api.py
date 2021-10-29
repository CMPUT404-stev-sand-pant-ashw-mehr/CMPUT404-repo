from comment.models import Comment
from author.models import Author
from post.models import Post
from rest_framework import status, viewsets
from .serializers import CommentSerializer
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
            Author.objects.exclude(user__isnull=True).get(id=author_id)
            Post.objects.get(id=post_id, author=author_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        Comment.objects.filter()

    def add_comment_to_post(self, request, author_id=None, post_id=None):
        pass
