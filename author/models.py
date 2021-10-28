from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User 
import uuid

class Author(models.Model):
    # ID of the Author
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)

    # foreign key to connect with the user auth table in django
    # If this field is null it indicates that the author is not a local user
    user = models.OneToOneField(User, on_delete=CASCADE, blank=True, null=True)

    # the home host of the author
    host = models.URLField(blank=True)

    # the display name of the author
    displayName = models.CharField(max_length=255)

    # url to the authors profile
    url = models.URLField(blank=True)

    # HATEOS url for Github API
    github = models.CharField(null= True, blank=True, max_length=255)

    # Image from a public domain
    profileImage = models.CharField(max_length=255, blank=True)

    
    def get_full_path(self):
        return str(self.host) + f"/author/{self.id}"
