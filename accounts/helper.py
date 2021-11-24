from .models import Node
from .serializers import NodeSerializer
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
    # test authors
    test_req = requests.get('https://cmput-404-socialdistribution.herokuapp.com/service/author/', auth=('socialdistribution_t18','c404t18'), headers={'Referer': "http://127.0.0.1:9000/"})
    if test_req.status_code == 500:
        pass
    else:
        j_req_test = test_req.json()
        authors = authors + j_req_test
    
    # foreign authors from team15
    team_15_req = requests.get('https://unhindled.herokuapp.com/service/authors/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_15_req.status_code == 500:
        pass
    else:
        j_req_15 = team_15_req.json()
        authors = authors + j_req_15
    
    # foreign authors from team17
    team_17_req = requests.get('https://unhindled.herokuapp.com/service/authors/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_17_req.status_code == 500:
        pass
    else:
        j_req_17 = team_17_req.json()
        authors = authors + j_req_17
    
    return authors


def get_list_foregin_posts():
    posts = []
    # test posts
    test_req = requests.get('https://cmput-404-socialdistribution.herokuapp.com/service/allposts/', auth=('socialdistribution_t18','c404t18'), headers={'Referer': "http://127.0.0.1:9000/"})
    if test_req.status_code == 500:
        pass
    else:
        j_req_test = test_req.json()
        test_posts = j_req_test['posts']
        posts = posts + test_posts
    
    # foreign posts from team15
    team_15_req = requests.get('https://unhindled.herokuapp.com/service/allposts/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_15_req.status_code == 500:
        pass
    else:
        j_req_15 = team_15_req.json()
        posts = posts + j_req_15
    
    # foreign posts from team17
    team_17_req = requests.get('https://unhindled.herokuapp.com/service/allposts/', auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:9000/"})
    if team_17_req.status_code == 500:
        pass
    else:
        j_req_17 = team_17_req.json()
        posts = posts + j_req_17
    
    
    return posts