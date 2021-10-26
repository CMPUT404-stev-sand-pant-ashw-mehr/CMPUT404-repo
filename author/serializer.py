from rest_framework import serializers

from author.models import Author

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']