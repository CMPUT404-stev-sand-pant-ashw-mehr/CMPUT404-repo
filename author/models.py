from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User 

class Author(models.Model):
    type =  models.CharField(max_length=255)

    local_user_id = models.ForeignKey(User, on_delete=CASCADE, null=True)

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
        unique_together = (("id", "local_user_id"),)