from rest_framework import serializers
from backend.models import Post, Comment, Inbox, Author

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


# https://www.django-rest-framework.org/api-guide/fields/#listfield
class InboxSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.JSONField(), default=list)

    class Meta:
        model = Inbox
        fields = ('id', 'author', 'items')


class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ['type', 'id', 'user','host', 'displayName', 'url', 'github', 'profileImage']
