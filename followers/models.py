from typing import Callable
from django.db import models
from django.db.models.deletion import CASCADE

# Followers
class Followers(models.Model):
    #Followers is a weak entity
    #Its primary key will be author id and follower id
    author_id = models.ForeignKey("author.Author", related_name="author_id", on_delete=CASCADE)

    class Meta:
        unique_together = (("author_id", "id"),)

    follower_id = models.ForeignKey("author.Author", related_name="follower_id", on_delete=CASCADE)

# Friend request
class FriendRequest(models.Model):
    summary = models.TextField()
    actor = models.ForeignKey("author.Author", related_name="actor", on_delete=CASCADE)
    receiver = models.ForeignKey("author.Author", related_name="object", on_delete=CASCADE)