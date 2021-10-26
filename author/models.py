from django.db import models
from django.contrib.auth.models import User 

class Author(models.Model):
    type =  models.CharField(max_length=255)

    # ID of the Author
    id = models.CharField(max_length=255, primary_key=True)

    # foreign key to connect with the user auth table in django
    uid = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

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