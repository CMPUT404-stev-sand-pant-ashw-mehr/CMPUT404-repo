from rest_framework import serializers
from post.models import Post
from author.models import Author
from comment.models import Comment

from django.forms.models import model_to_dict

# Post Serializer 
class PostSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Post 
        fields = (
            'type', 
            'id',
            'title', 
            'source', 
            'origin', 
            'description', 
            'contentType', 
            'content', 
            'categories', 
            'published',
            'visibility',
            'unlisted'    
        )
    