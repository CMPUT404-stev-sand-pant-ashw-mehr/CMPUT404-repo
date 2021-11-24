from rest_framework import serializers
from author.models import Author
from author.serializer import AuthorSerializer
from .models import Followers

class FollowerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ("author", "follower", "follow_date")
        