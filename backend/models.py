from django.db import models

# sample model
class Posts(models.Model):
    author = models.CharField(max_length=30)
    data_type = models.CharField(max_length=30)
    data = models.CharField(max_length=30)
