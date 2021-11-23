from django.db import models

# Create your models here.

class Node(models.Model):
    host = models.CharField(max_length=150)
    

