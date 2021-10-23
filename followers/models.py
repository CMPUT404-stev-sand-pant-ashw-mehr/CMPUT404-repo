from django.db import models
from django.db.models.base import Model
from social_distribution.author.models import Author

# Followers
class Followers(models.Model):
    #Followers is a weak entity
    #Its primary key will be author id and follower id
    author_id = models.ForeignKey(Author, related_name="author_id")

    class Meta:
        unique_together = (("author_id", "id"),)

    follower_id = models.ForeignKey(Author, related_name="follower_id")

# Friend request
class FriendRequest(models.Model):
    summary = models.TextField()
    actor = models.ForeignKey(Author, related_name="actor")
    receiver = models.ForeignKey(Author, related_name="object")