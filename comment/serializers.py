from rest_framework import serializers
from comment.models import Comment
from author.models import Author
from django.forms.models import model_to_dict

# Comment Serializer 
class CommentSerializer(serializers.ModelSerializer): 
    author = serializers.SerializerMethodField()

    class Meta: 
        model = Comment
        # fields = '__all__'
        exclude = ('post',)

    def get_author(self, obj) -> dict():
        author_query = Author.objects.get(id=obj.author)
        author_details = model_to_dict(author_query)
        author_details['id'] = author_details['url']
        return author_details
    