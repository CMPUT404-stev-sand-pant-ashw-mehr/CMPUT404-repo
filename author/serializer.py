from rest_framework import serializers

from author.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'type', 'host', 'url','displayName', 'github', 'profileImage']
        read_only_fields = ['type']
