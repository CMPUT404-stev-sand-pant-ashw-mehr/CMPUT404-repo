from rest_framework import serializers
from inbox.models import Inbox

class InboxSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="inbox_author_id")

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')
        