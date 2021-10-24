from rest_framework import serializers
from author.models import Author
from author.serializer import AuthorSerializer
from .models import Followers, FriendRequest

class FollowerSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="followers") # This indicates the type of the JSON
    items = AuthorSerializer(many=True, read_only=True) # This is the nested list of followers

    class Meta:
        model = Followers
        fields = ("type", "items")

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


class FriendRequestSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="Follow") # This indicates that it is a follow request
    actor = AuthorSerializer(read_only=True)
    object_ = AuthorSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "receiver")

    # Override
    # Rename "receiver" field to "object"
    def get_fields(self) -> dict():
        #Rename the field receiver to object, since object is a python keyword it cannot be used in model
        result = super().get_fields()
        object_ = result.pop("receiver")
        result["object"] = object_
        return result
    
    # Override
    # receive author, summary and follower.
    def create(self, validated_data):
        follower = validated_data.pop("actor")
        followee = validated_data.pop("object")
        summary = validated_data.pop("summary")
        actor = follower.pop("url")
        receiver = followee.pop("url")

        return FriendRequest.objects.create(summary=summary, actor=actor, receiver=receiver)
