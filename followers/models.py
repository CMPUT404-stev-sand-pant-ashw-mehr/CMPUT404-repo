from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Followers
class Followers(models.Model):
    #Followers is a weak entity
    #Its primary key will be author id and follower id
    author_id = models.ForeignKey(User, related_name="author_id", on_delete=CASCADE)
    follower_id = models.ForeignKey(User, related_name="follower_id", on_delete=CASCADE)

    class Meta:
        unique_together = (("author_id", "follower_id"),)

# Friend request
class FriendRequest(models.Model):
    summary = models.TextField()
    actor = models.ForeignKey(User, related_name="actor", on_delete=CASCADE)
    receiver = models.ForeignKey(User, related_name="object", on_delete=CASCADE)