from django.db import models
import uuid
from author.models import Author
from post.models import Post
from django.utils import timezone 

# Create your models here.
class Comment(models.Model):
    # ID of the Comment (UUID)
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4().hex, editable=False)
    
    type = models.CharField(max_length=255, default = "comment")
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    comment = models.TextField()
    
    contentType = models.CharField(max_length=255, default = "text/markdown")
    
    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.comment)

    def save(self, *args, **kwargs):
        self.id = uuid.uuid4().hex
        super(Comment, self).save(args, kwargs)
