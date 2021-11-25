from django.test import TestCase
from django.test.client import Client
from knox.models import AuthToken
from django.contrib.auth.models import User
from author.models import Author
from post.models import Post

# Create your tests here.
class PostTest(TestCase):
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
    
    def test_create_post_POST(self):
        test_post = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "description":"This post discusses stuff -- brief",
            "categories": str(['test1', 'test2']),
            "contentType":"text/plain",
            "content":"Test content",
            "count": 1023,
            "visibility":"PUBLIC",
            "unlisted": 'false'
        }

        r = self.client.post('/author/1/posts', test_post)
        self.assertTrue(200 <= r.status_code < 300)

        post_id = r.json()['id']
        self.assertTrue(Post.objects.filter(id=post_id).exists())
    
    def test_create_post_PUT(self):
        test_post = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "categories": str(['test1', 'test2']),
            "contentType":"text/plain",
            "content":"Test content",
            "count": 1023,
            "visibility":"PUBLIC",
            "unlisted": 'false'
        }
        r = self.client.put('/author/1/posts/2', data=test_post, content_type="application/json")
        self.assertTrue(200 <= r.status_code < 300)

    def test_delete_post(self):
        test_post = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "categories": str(['test1', 'test2']),
            "contentType":"text/plain",
            "content":"Test content",
            "count": 1023,
            "visibility":"PUBLIC",
            "unlisted": 'false'
        }

        r = self.client.post('/author/1/posts', test_post)

        post_id = r.json()['id']
        self.assertTrue(Post.objects.filter(author='1', id=post_id).exists())
        r = self.client.delete(f'/author/1/posts/{post_id}/')
        self.assertTrue(200 <= r.status_code < 300)

    def test_get_post(self):
        test_post = {
            "type":"post",
            "title":"A post title about a post about web dev",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "categories": str(['test1', 'test2']),
            "contentType":"text/plain",
            "content":"Test content",
            "count": 1023,
            "visibility":"PUBLIC",
            "unlisted": 'false'
        }

        r = self.client.post('/author/1/posts', test_post)

        post_id = r.json()['id']

        r = self.client.get('/author/1/posts/' + post_id)
        self.assertTrue(200 <= r.status_code < 300)