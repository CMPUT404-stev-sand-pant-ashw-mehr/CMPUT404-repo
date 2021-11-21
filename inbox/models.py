from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from author.models import Author
from post.models import Post
from followers.models import FriendRequest
from likes.models import Like
from comment.models import Comment

class Inbox(models.Model):
    type = models.CharField(max_length=10, default="inbox")

    author = models.ForeignKey(Author, related_name="owner", on_delete=models.CASCADE)

    post_item = models.ForeignKey(Post, related_name="inbox_post", on_delete=models.CASCADE, blank=True, null=True)

    like_item = models.ForeignKey(Like, related_name="inbox_like", on_delete=models.CASCADE, blank=True, null=True)

    follow_item = models.ForeignKey(FriendRequest, related_name="inbox_request", on_delete=models.CASCADE, blank=True, null=True)

    def clean(self) -> None:
        if not (self.post_item or self.like_item or self.follow_item):
            raise ValidationError("Item has to be either a post, like or follow")
        return super().clean()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(post_item__isnull=False) &
                    Q(like_item__isnull=True) &
                    Q(follow_item__isnull=True)
                ) | (
                    Q(post_item__isnull=True) &
                    Q(like_item__isnull=False) &
                    Q(follow_item__isnull=True)
                ) | (
                    Q(post_item__isnull=True) &
                    Q(like_item__isnull=True) &
                    Q(follow_item__isnull=False)
                ),
                name="only_one_item_type",
            )
        ]