from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 

class Post(models.Model):
    postType = models.CharField(max_length=255)
    # title of a post
    title = models.TextField()
    # id of the post
    # id = done by default
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
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
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

# GET List of Posts
class Inbox(models.Model):
    '''
    Retrieves all new posts sent to this author

    Inbox model:
        author/sender      Who's Inbox this is
    '''
    # Suppose to be Author or User?
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # I'm retrieving these items? Could group items into a JSONField
    # post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_id')

    # follow = models.ForeignKey(Follow, on_delete=models.CASCADE, related_name='follow')
    # like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='like')
    # comments = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='comments')
    # # automatically sets the timestamp of when the object was first created. 
    # published = models.DateTimeField(auto_now_add=True)

# For POSTing all posts
class Inbox_Item(models.model):
    inbox_id = models.ForeignKey(Inbox, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=255)
    item_id = models.ForeignKey(item_type, on_delete=models.CASCADE, related_name='item_id')
