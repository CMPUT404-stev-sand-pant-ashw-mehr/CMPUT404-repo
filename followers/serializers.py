from django.db import models
from rest_framework import serializers
from Project.social_distribution.author.serializer import AuthorSerializer
from models import Followers

class FollowerSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default="followers")
    items = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Followers
        field = ("type", "items")