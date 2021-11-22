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
