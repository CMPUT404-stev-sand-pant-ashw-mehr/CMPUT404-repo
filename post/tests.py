from django.test import TestCase
from django.test.client import Client
from knox.models import AuthToken
from django.contrib.auth.models import User
from author.models import Author

# Create your tests here.
class FollowerTest(TestCase):
    def setUp(self) -> None:
        # create test user for login
        self.testUserAuthed = User.objects.create(id=1, username="testUser1", password="1234")
        token = AuthToken.objects.create(user=self.testUserAuthed)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token[1])
        self.client.login(username="testUser1", password="1234")

        # create test user 1, 2, 3
        # test user 2, 3, follows 1

        self.testUser1 = {
            "type" : "author",
            "id": "1",
            "user": self.testUserAuthed,
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser1",
            "url": "http://127.0.0.1:8000/author/1",
            "github": "https://github.com/testUser1",
            "profileImage":"None"
        }

        self.testUser2 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/2",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser2",
            "url": "http://127.0.0.1:8000/author/2",
            "github": "https://github.com/testUser2",
            "profileImage":"None"
        }

        self.testUser3 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/3",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser3",
            "url": "http://127.0.0.1:8000/author/3",
            "github": "https://github.com/testUser3",
            "profileImage":"None"
        }

        self.testUser1Obj = Author.objects.create(**self.testUser1)
        self.testUser2Obj = Author.objects.create(**self.testUser2)
        self.testUser3Obj = Author.objects.create(**self.testUser3)

        Followers.objects.create(author=self.testUser1Obj, follower=self.testUser2Obj)
        Followers.objects.create(author=self.testUser1Obj, follower=self.testUser3Obj)