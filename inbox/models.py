from django.db import models
from author.models import Author
from django.contrib.postgres.fields import ArrayField


class Inbox(models.Model):
    type = models.CharField(max_length=10, default="inbox")

    inbox_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    items = ArrayField(models.JSONField(), default=list)

