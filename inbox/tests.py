from django.test import TestCase
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.test.client import Client
from author.models import Author
import json

class InboxTest(TestCase):
    def setUp(self) -> None:
        # create test user for login
        self.testUserAuthed = User.objects.create(id=1, username="testUser1", password="1234")
        token = AuthToken.objects.create(user=self.testUserAuthed)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token[1])
        self.client.login(username="testUser1", password="1234")


        self.testUser1 = {
            "type" : "author",
            "id": "1",
            "user": self.testUserAuthed,
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser1",
            "url": "http://127.0.0.1:8000/author/1",
            "github": "https://github.com/testUser1",
            "profileImage":"None",
            "is_active": True
        }

        self.testUser2 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/2",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser2",
            "url": "http://127.0.0.1:8000/author/2",
            "github": "https://github.com/testUser2",
            "profileImage":"None",
            "is_active": True
        }

        self.testUser3 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/3",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser3",
            "url": "http://127.0.0.1:8000/author/3",
            "github": "https://github.com/testUser3",
            "profileImage":"None",
            "is_active": True
        }

        self.testUser1Obj = Author.objects.create(**self.testUser1)
        self.testUser2Obj = Author.objects.create(**self.testUser2)
        self.testUser3Obj = Author.objects.create(**self.testUser3)

    def test_inbox(self):
        # test for invalid inbox items
        postData = {
            "empty": 0
        }

        r = self.client.post('/author/1/inbox', data=postData)
        self.assertEqual(r.status_code, 400)

        # test for valid inbox item
        postData = {
            "type": "Follow",      
            "summary":"Greg wants to follow Lara",
            "actor": json.dumps({
                "type" : "author",
                "id": "http://127.0.0.1:8000/author/2",
                "host": "http://127.0.0.1:8000/",
                "displayName": "TestUser2",
                "url": "http://127.0.0.1:8000/author/2",
                "github": "https://github.com/testUser2",
                "profileImage":"None"
            }),
            "object": json.dumps({
                "type" : "author",
                "id": "http://127.0.0.1:8000/author/1",
                "host": "http://127.0.0.1:8000/",
                "displayName": "TestUser1",
                "url": "http://127.0.0.1:8000/author/1",
                "github": "https://github.com/testUser1",
                "profileImage":"None"
            })
        }
        r = self.client.post('/author/1/inbox', data=postData)
        self.assertTrue(200 <= r.status_code < 300)

        # test if inbox is updated
        r = self.client.get('/author/1/inbox')
        self.assertTrue(200 <= r.status_code < 300)

        data = r.json()
        self.assertEqual(len(data['items']), 1)

        # test clear inbox
        r = self.client.delete('/author/1/inbox')
        self.assertTrue(200 <= r.status_code < 300)

        # test if items are cleared
        r = self.client.get('/author/1/inbox')
        self.assertTrue(200 <= r.status_code < 300)
        data = r.json()
        self.assertEqual(len(data['items']), 0)

    def test_format_validation(self):
        postData = {
            "type":"post",
            "title":"DID YOU READ MY POST YET?",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/999999983dda1e11db47671c4a3bbd9e",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"Whatever",
            "contentType":"text/plain",
            "content":"Are you even reading my posts Arjun?",
            "author":json.dumps({
                  "type":"author",
                  "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                  "host":"http://127.0.0.1:5454/",
                  "displayName":"Lara Croft",
                  "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                  "github": "http://github.com/laracroft",
                  "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }),
            "categories":'["web","tutorial"]',
            "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"FRIENDS",
            "unlisted":'false'
        }

        r = self.client.post('/author/1/inbox', data=postData)
        self.assertTrue(200 <= r.status_code < 300)

        likeData = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Lara Croft Likes your post",         
            "type": "Like",
            "author":json.dumps({
                "type":"author",
                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github":"http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }),
            "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
        }

        r = self.client.post('/author/1/inbox', data=likeData)
        self.assertTrue(200 <= r.status_code < 300)

        invalidData = {
            "fail": "Shouldn't pass"
        }

        r = self.client.post('/author/1/inbox', data=invalidData)
        self.assertTrue(400 <= r.status_code < 500)

        invalidData = {
            "type": "post",
            "fail": "shouldn't pass"
        }

        r = self.client.post('/author/1/inbox', data=invalidData)
        self.assertTrue(400 <= r.status_code < 500)