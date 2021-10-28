from rest_framework import serializers
from comment.models import Comment

# Comment Serializer 
class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = '__all__'
        read_only_fields = ('uuid', 'published')
        