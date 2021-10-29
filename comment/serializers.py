from rest_framework import response, serializers
from comment.models import Comment
from author.serializer import AuthorSerializer
from django.forms.models import model_to_dict

# Comment Serializer 
class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = ('id', 'type', 'author', 'comment', 'contentType', 'published')