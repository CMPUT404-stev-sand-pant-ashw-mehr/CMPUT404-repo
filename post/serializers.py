from rest_framework import serializers
from post.models import Post, Comment

# Post Serializer 
class PostSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Post 
        fields = '__all__'
        
# Comment Serializer 
class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = '__all__'
        read_only_fields = ('uuid', 'published')