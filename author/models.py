from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User 
import uuid

class Author(models.Model):
    type =  models.CharField(max_length=255)

    # ID of the Author
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)

    # foreign key to connect with the user auth table in django
    # If this field is null it indicates that the author is not a local user
    uid = models.ForeignKey(User, on_delete=CASCADE, blank=True, null=True)

    # the home host of the author
    host = models.CharField(max_length=255)

    # the display name of the author
    displayName = models.CharField(max_length=255)

    # url to the authors profile
    url = models.CharField(max_length=255)

    # HATEOS url for Github API
    github = models.CharField(max_length=255)

    # Image from a public domain
    profileImage = models.CharField(max_length=255)

    class Meta:
        unique_together = (("id", "url"),)