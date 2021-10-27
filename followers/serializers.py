from rest_framework import serializers
from author.models import Author
from author.serializer import AuthorSerializer
from .models import Followers, FriendRequest

class FollowerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ("author", "follower")

class FriendRequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("summary", "actor", "receiver")
        