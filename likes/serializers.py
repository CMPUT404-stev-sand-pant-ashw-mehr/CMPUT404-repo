from rest_framework import serializers
from post.models import Post
from author.models import Author
from comment.models import Comment
from likes.models import Like

from django.forms.models import model_to_dict

# Post Serializer 
class LikeSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Like 
        fields = (
            'type', 
            'author',
            'object'
        )
