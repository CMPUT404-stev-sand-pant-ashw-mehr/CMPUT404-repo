from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from author.models import Author
from knox.models import AuthToken
from comment.api import CommentViewSet

# Create your tests here.
class CommentTest(TestCase):
    def setUp(self) -> None:
        # create test user for login
        self.testUserAuthed = User.objects.create(
            id=1, username="testUser1", password="1234")
        token = AuthToken.objects.create(user=self.testUserAuthed)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token[1])
        self.client.login(username="testUser1", password="1234")

        self.testUser2Authed = User.objects.create(
            id=2, username="testUser2", password="1234")

        # Test user 1, 2 are local user, while test user 3 is a foreign author
        self.testUser1 = {
            "type": "author",
            "id": "1",
            "user": self.testUserAuthed,
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser1",
            "url": "http://127.0.0.1:8000/author/1",
            "github": "https://github.com/testUser1",
            "profileImage": "None",
            "is_active": True
        }

        self.testUser1Obj = Author.objects.create(**self.testUser1)

        test_post = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "categories": str(['test1', 'test2']),
            "contentType":"text/plain",
            "content":"Test content",
            "visibility":"PUBLIC",
            "unlisted": 'false'
        }

        r = self.client.post('/author/1/posts', test_post)

        self.post_id = r.json()['id']
    
    def test_comment(self):
        test_comment = {
            "type": "comment",
            "comment": "This is a test comment",
            "contentType": "text/plain"
        }

        r = self.client.post(f'/author/1/posts/{self.post_id}/comments', data=test_comment)
        self.assertTrue(200 <= r.status_code < 300)
        r = self.client.post(f'/author/1/posts/{self.post_id}/comments', data=test_comment)
        self.assertTrue(200 <= r.status_code < 300)
        r = self.client.get(f'/author/1/posts/{self.post_id}/comments')
        self.assertTrue(200 <= r.status_code < 300)
        