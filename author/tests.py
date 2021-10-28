from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from author.models import Author
from knox.models import AuthToken

# Create your tests here.
class AuthorTest(TestCase):
    def setUp(self) -> None:
        # create test user for login
        self.testUserAuthed = User.objects.create(id=1, username="testUser1", password="1234")
        token = AuthToken.objects.create(user=self.testUserAuthed)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token[1])
        self.client.login(username="testUser1", password="1234")

        self.testUser2Authed = User.objects.create(id=2, username="testUser2", password="1234")

        # Test user 1, 2 are local user, while test user 3 is a foreign author
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
            "id": "2",
            "user": self.testUser2Authed,
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

    def test_get_all_authors(self):
        r = self.client.get('/authors/')
        
        try:
            result = r.json()
        except:
            self.assertTrue(False, "result does not contain JSON data")

        self.assertEquals(type(result), dict)

        self.assertTrue('type' in result.keys())
        self.assertTrue('items' in result.keys())

        self.assertEquals(result['type'].strip(), 'authors')

        authors = result['items']

        self.assertEquals(len(authors), 2)

        self.assertEquals(authors[0]['id'], authors[0]['url'])
        self.assertEquals(authors[1]['id'], authors[1]['url'])

        self.assertEquals(authors[0]['url'], self.testUser1['url'])
        self.assertEquals(authors[1]['url'], self.testUser2['url'])
        