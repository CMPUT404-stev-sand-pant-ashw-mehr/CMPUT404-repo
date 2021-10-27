from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from author.models import Author

# Followers
class Followers(models.Model):
    # Followers is a weak entity
    # Its primary key will be author id and follower id
    # author id is the person being followed
    author = models.ForeignKey(Author, related_name="author", on_delete=CASCADE)
    # follower url is the url of the follower
    follower = models.ForeignKey(Author, related_name="follower", on_delete=CASCADE)
    # date which the author is followed
    follow_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        unique_together = (("author", "follower"),)


# Friend request
class FriendRequest(models.Model):
    # Summary of the action
    summary = models.TextField()
    # The person sending the request
    actor = models.JSONField()
    # The receiver. Named "object" in the spec. 
    receiver = models.JSONField()

    request_date = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        unique_together = (("actor", "receiver"),)