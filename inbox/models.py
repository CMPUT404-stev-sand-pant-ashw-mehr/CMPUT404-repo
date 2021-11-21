from django.db import models
from django.db.models import Q
from author.models import Author
from django.contrib.postgres.fields import ArrayField


class Inbox(models.Model):
    type = models.CharField(max_length=10, default="inbox")

    author = models.ForeignKey(Author, related_name="owner", on_delete=models.CASCADE)

    inbox_items = ArrayField(models.JSONField(), default=list)
