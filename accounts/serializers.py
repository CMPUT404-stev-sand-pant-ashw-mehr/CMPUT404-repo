from author.serializer import AuthorSerializer
from rest_framework import serializers 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from author.models import Author
from . models import Node

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        # add 'email' back
        fields = ('id', 'username', 'password', 'author',)
        extra_kwargs = {'password': {'write_only': True}}

    # 
    def retrieve_author(self, object):
        try:
            author = object.author
            return AuthorSerializer(author).data
        except:
            return None

class RegisterSerializer(serializers.ModelSerializer):
    
    displayName = serializers.CharField(required=True, max_length = 255)
    github = serializers.URLField(allow_blank=True, required= False)
    
    class Meta: 
        model = User 
        fields = ('id', 'username', 'email', 'password', 'displayName', 'github')
        extra_kwargs = { 'password': {'write_only': True}}

    def validate(self, validated_data):
        author = Author.objects.filter(displayName=validated_data['displayName'])
        
        if author.exists():
            raise serializers.ValidationError(
                'Display name taken!'
            )
        else:
            return validated_data
        
    def create(self, data):
        user = User.objects.create_user(
            username=data['username']
        )

        user.set_password(data['password'])
        user.save()

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if not user:
            raise serializers.ValidationError("Incorrect username or password.")
        
        return data
    
class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['host']

