from rest_framework import serializers
from author.models import Author
from author.serializer import AuthorSerializer
from .models import Followers, FriendRequest

class FollowerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ("author_id", "follower_url")

class FollowerAPISerializer(serializers.Serializer):
    type = serializers.ReadOnlyField(default="followers") # This indicates the type of the JSON
    items = AuthorSerializer(many=True, read_only=True) # This is the nested list of followers

    def create(self, validated_data):
        return super().create(validated_data)

    # Create an entry from a friend request
    def create_from_friend_request(self, validated_data):
        follower = validated_data.pop("actor")
        followee = validated_data.pop("object")
        author_id = followee["url"]
        follower_url = follower["url"]

        # Check if author_id exists in Author table. If not, create entry
        if not Author.objects.filter(id=author_id).exists():
            Author.objects.create(**followee)

        return Followers.objects.create(author_id=author_id, follower_url=follower_url)

class FriendRequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("summary", "actor", "receiver")

class FriendRequestAPISerializer(serializers.Serializer):
    type = serializers.ReadOnlyField(default="Follow") # This indicates that it is a follow request
    actor = AuthorSerializer(read_only=True)
    receiver = AuthorSerializer(read_only=True)
    
    # Override
    # receive author, summary and follower.
    def create(self, validated_data):
        follower = validated_data.pop("actor")
        followee = validated_data.pop("object")
        summary = validated_data.pop("summary")
        actor = follower.pop("url")
        receiver = followee.pop("url")

        return FriendRequest.objects.create(summary=summary, actor=actor, receiver=receiver)
