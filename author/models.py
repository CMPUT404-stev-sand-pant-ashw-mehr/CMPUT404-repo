from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User 

class Author(models.Model):

    type = models.CharField(max_length=255, default="author")
    # ID of the Author
    id = models.CharField(unique=True, primary_key=True, max_length=255, null=False, blank=False)

    # foreign key to connect with the user auth table in django
    # If this field is null it indicates that the author is not a local user
    user = models.OneToOneField(User, on_delete=CASCADE, blank=True, null=True)

    # the home host of the author
    host = models.URLField(blank=False)

    # the display name of the author
    displayName = models.CharField(max_length=255)

    # url to the authors profile
    url = models.URLField(blank=False)

    # HATEOS url for Github API
    github = models.CharField(null= True, blank=True, max_length=255)

    # Image from a public domain
    profileImage = models.CharField(max_length=255, blank=True)



    # using this to get full path for author
    def get_full_path(self):
        return self.host + f"api/author/{self.id}/"