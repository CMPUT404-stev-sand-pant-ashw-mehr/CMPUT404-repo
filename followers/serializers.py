from rest_framework import serializers
from author.serializer import AuthorSerializer
from .models import Followers, FriendRequest

class FollowerSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="followers") # This indicates the type of the JSON
    items = AuthorSerializer(many=True, read_only=True) # This gets the list of followers

    class Meta:
        model = Followers
        fields = ("type", "items")


class FriendRequestSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="Follow") # This indicates that it is a follow request
    actor = AuthorSerializer(read_only=True)
    object_ = AuthorSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "receiver")

    #Override
    def get_fields(self) -> dict():
        #Rename the field receiver to object, since object is a python keyword it cannot be used in model
        result = super().get_fields()
        object_ = result.pop("receiver")
        result["object"] = object_
        return result