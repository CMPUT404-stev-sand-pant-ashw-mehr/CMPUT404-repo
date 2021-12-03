from requests.models import Response
from .models import Node
from .serializers import NodeSerializer
from author.models import Author
from author.serializer import AuthorSerializer
import requests

def get_valid_nodes():
    nodes = Node.objects.all()
    node_serializer = NodeSerializer(nodes, many=True)
    valid_nodes = []
    for n in node_serializer.data:
        valid_nodes.append(n["host"])
    return valid_nodes

def is_valid_node(request):
    host = request.build_absolute_uri("/")
    if host not in ['http://127.0.0.1:8000/',
                    'http://localhost:8000/',
                    'https://social-dis.herokuapp.com/',
                    'http://testserver/',
                    'http://127.0.0.1:9000/',
                    'http://localhost:9000/',]:
        # check valid node
        valid_nodes = get_valid_nodes()
        if host not in valid_nodes:
            return False
    return True


def get_list_foregin_authors():
    authors = []
    # foreign authors from team15
    team_15_req = requests.get('https://unhindled.herokuapp.com/service/authors/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if not (200 <= team_15_req.status_code < 300):
        pass
    else:
        j_req_15 = team_15_req.json()['items']
        authors = authors + j_req_15
    
    # foreign authors from team17
    team_17_req = requests.get('https://cmput404f21t17.herokuapp.com/service/connect/public/author/', auth=('4cbe2def-feaa-4bb7-bce5-09490ebfd71a','123456'), headers={'Referer': "http://127.0.0.1:9000/"})
    if not (200 <= team_17_req.status_code < 300):
        pass
    else:
        j_req_17 = team_17_req.json()['items']
        authors = authors + j_req_17
        
    # foreign authors from team14
    team_14_req = requests.get('https://linkedspace-staging.herokuapp.com/api/authors/', auth=('socialdistribution_t14','c404t14'), headers={'Referer': "http://127.0.0.1:9000/"})
    if not (200 <= team_14_req.status_code < 300):
        pass
    else:
        j_req_14 = team_14_req.json()['items']
        authors = authors + j_req_14
    
    return authors

def get_foregin_author_detail(author_id):
    authors = get_list_foregin_authors()
    for author in authors:
        author["uuid"] = author["id"].split("/")[-1]
        if author['uuid'] == author_id:
            return (author)
    return "author not found!"


def get_list_foregin_posts():
    posts = []
    # foreign posts from team15
    team_15_req = requests.get('https://unhindled.herokuapp.com/service/allposts/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_15_req.status_code == 500:
        pass
    else:
        j_req_15 = team_15_req.json()
        posts = posts + j_req_15
    
    # foreign posts from team17
    team_17_req = requests.get('https://cmput404f21t17.herokuapp.com/service/connect/public/', auth=('4cbe2def-feaa-4bb7-bce5-09490ebfd71a','123456'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_17_req.status_code in (500, 404, 503, 200):
        pass
    else:
        j_req_17 = team_17_req.json()['items']
        posts = posts + j_req_17
        
    # foreign posts from team14
    team_17_req = requests.get('https://linkedspace-staging.herokuapp.com/api/posts/', auth=('socialdistribution_t14','c404t14'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_17_req.status_code in (500, 404):
        pass
    else:
        j_req_17 = team_17_req.json()
        posts = posts + j_req_17
    
    for post in posts:
        post["uuid"] = ""
        if post["id"][-1] == "/":
            post["id"] = post["id"][:-1]
        post["uuid"] = post["uuid"] = post["id"].split("/")[-1]
    return posts

def get_foregin_public_post_detail(post_id):
    posts = get_list_foregin_posts()
    for post in posts:
        post["uuid"] = ""
        if post["id"][-1] == "/":
            post["id"] = post["id"][:-1]
        post["uuid"] = post["id"].split("/")[-1]
        if post["uuid"] == post_id:
            return post
    return "post not found!"

def send_friend_request(local_author_id, foreign_author_id):
    try:
        author = Author.objects.get(id=local_author_id)
    except:
        return "author not found!"
    
    return_data = {
        "type": "Follow",
    }
    author_data = AuthorSerializer(author).data
    local_author_name = author_data["displayName"]

    return_data["actor"] = author_data

    foreign_authors = get_list_foregin_authors()
    for foreign_author in foreign_authors:
        if foreign_author["id"].strip()[-1] == '/':
            foreign_author["id"] = foreign_author["id"].strip()[:-1]
        
        if foreign_author_id[-1] == '/':
            foreign_author_id = foreign_author_id[:-1]

        if foreign_author["id"] == foreign_author_id:
            return_data["object"] = foreign_author

            try:
                foreign_author_name = foreign_author["displayName"]
            except:
                foreign_author_name = ""

            break
    else:
        return "foreign author not found!"

    return_data["summary"] = f"{local_author_name} wants to follow {foreign_author_name}"

    return return_data

