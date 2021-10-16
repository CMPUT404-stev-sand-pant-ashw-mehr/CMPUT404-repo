from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 

class Author(models.Model):
    type =  models.CharField(max_length=255)

    # ID of the Author
    id=	models.PositiveIntegerField()

    # the home host of the author
    host = models.CharField(max_length=255)

    # the display name of the author
    displayName = models.CharField(max_length=255)

    # url to the authors profile
    url = models.CharField(max_length=255)

    # HATEOS url for Github API
    githubLink = models.CharField(max_length=255)

    # Image from a public domain
    profileImageLink = models.CharField(max_length=255)