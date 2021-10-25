from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from author.models import Author

# Followers
class Followers(models.Model):
    #Followers is a weak entity
    #Its primary key will be author id and follower id
    #author id is the person being followed
    author_id = models.ForeignKey(Author, related_name="author_id", on_delete=CASCADE)
    #follower url is the url of the follower
    follower_url = models.JSONField()
    # date which the author is followed
    follow_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        unique_together = (("author_id", "follower_url"),("author_id", "id"))

    

# Friend request
class FriendRequest(models.Model):
    # Summary of the action
    summary = models.TextField()
    # The person sending the request
    actor = models.JSONField()
    # The url of the receiver. Named "object" in the spec. 
    receiver = models.JSONField()

    request_date = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        unique_together = (("actor", "receiver"),)