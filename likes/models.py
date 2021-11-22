from django.db import models
from author.models import Author
from comment.models import Comment
from post.models import Post

class Like(models.Model):
    
    id = models.CharField(primary_key=True, max_length=255, blank=False, null=False)
    
    type = models.CharField(max_length=255, default='Like')
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    
    object =  models.CharField(max_length=255)
    
    class Meta:
        unique_together = (('author', 'post'), ('author', 'comment'))
        
    def __str__(self):
        return str(self.author)

