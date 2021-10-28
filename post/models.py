from django.db import models
from django.utils import timezone 
import uuid
from author.models import Author

class Post(models.Model):
    postType = models.CharField(max_length=255)
    # title of a post
    title = models.TextField()
    # id of the post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # where did you get this post from?
    source = models.TextField()
    # where is it actually from
    origin = models.TextField()
    # a brief description of the post
    description = models.TextField()
    # The content type of the post
    # assume either
    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64 # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
    # image/jpeg;base64 # this is an embedded jpeg
    # for HTML you will want to strip tags before displaying
    contentType = models.CharField(max_length=255)
    content = models.TextField()
    # the author has an ID where by authors can be disambiguated
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)
    # categories this post fits into (a list of strings
    # categories = many to many relationship
    # comments about the post
    # return a maximum number of comments
    # total number of comments for this post
    # count = calculated/loaded value
    # the first page of comments
    # comments = calculated/loaded value
    # commentsSrc is OPTIONAL and can be missing
    # You should return ~ 5 comments per post.
    # should be sorted newest(first) to oldest(last)
    # this is to reduce API call counts
    # commentSrc = calculated/loaded value
    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(default=timezone.now)
    # visibility ["PUBLIC","FRIENDS"]
    visibility = models.CharField(max_length=255)
    # for visibility PUBLIC means it is open to the wild web
    # FRIENDS means if we're direct friends I can see the post
    # FRIENDS should've already been sent the post so they don't need this
    unlisted = models.BooleanField()
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines


class Comment(models.Model):
    # ID of the Comment (UUID)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    commentType = models.CharField(max_length=255, default = "comment")
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    comment = models.TextField()
    
    contentType = models.CharField(max_length=255, default = "text/markdown")
    
    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.comment)