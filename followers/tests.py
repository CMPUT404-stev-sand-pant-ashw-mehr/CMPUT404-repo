from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.test.client import Client
from followers.models import Followers
from author.models import Author
from knox.models import AuthToken

# Test for Follower Model and its API
class FollowerTest(LiveServerTestCase):
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

    def test_followers_field(self):
        followers = Followers.objects.filter(author=self.testUser1["id"]).values()
        self.assertEquals(2, len(followers))
        
        for follower in followers:
            follower_id = follower["follower_id"]
            self.assertTrue(Author.objects.filter(id=follower_id).exists())
        
    
    def test_get_followers(self):
        r = self.client.get('/author/1/followers/')
        try:
            response = r.json()
            self.assertTrue(type(response)==dict)
        except TypeError:
            self.assertTrue(False, "No JSON is returned!")

        self.assertTrue("type" in response.keys())
        self.assertTrue("items" in response.keys())

        followers_item = response["items"]
        self.assertTrue(type(followers_item)==list)
        self.assertEquals(len(followers_item), 2)

    def test_put_follower(self):
        testUser4 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/4/",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser3",
            "url": "http://127.0.0.1:8000/author/4/",
            "github": "https://github.com/testUser4/",
            "profileImage":"None"
        }

        r = self.client.put('/author/1/followers/http://127.0.0.1:8000/author/4/', testUser4, content_type='application/json')
        follower_id = r.json()["follower"]

        self.assertTrue(Followers.objects.filter(follower=follower_id).exists())

        # GET the list of followers again for author 1 and check if followers is stored
        r = self.client.get('/author/1/followers/')

        followers_item = r.json()["items"]

        self.assertTrue(any(follower["id"] == follower_id for follower in followers_item))


    def test_delete_follower(self):
        testUser4 = {
            "type" : "author",
            "id": "http://127.0.0.1:8000/author/4",
            "host": "http://127.0.0.1:8000/",
            "displayName": "TestUser3",
            "url": "http://127.0.0.1:8000/author/4",
            "github": "https://github.com/testUser4",
            "profileImage":"None"
        }

        r = self.client.put('/author/1/followers/http://127.0.0.1:8000/author/4/', testUser4, content_type='application/json')
        self.assertTrue(200 <= r.status_code < 300) # Check if the response is a 2XX code

        r = self.client.delete('/author/1/followers/http://127.0.0.1:8000/author/4/')
        self.assertTrue(200 <= r.status_code < 300)

        self.assertFalse(Followers.objects.filter(follower=testUser4["id"]).exists())

    def test_check_follower(self):
        # Test user 1 and 2 should exists
        r = self.client.get('/author/1/followers/http://127.0.0.1:8000/author/2/')
        self.assertTrue(200 <= r.status_code < 300)

        r = self.client.get('/author/1/followers/http://127.0.0.1:8000/author/3/')
        self.assertTrue(200 <= r.status_code < 300)

        # Test user 5 should not exists
        r = self.client.get('/author/1/followers/http://127.0.0.1:8000/author/5/')
        self.assertTrue(400 <= r.status_code < 500)
