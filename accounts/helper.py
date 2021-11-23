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
    req = requests.get('https://cmput-404-socialdistribution.herokuapp.com/service/author/', auth=('socialdistribution_t18','c404t18'), headers={'Referer': "http://127.0.0.1:9000/"})
    j_req = req.json()
    authors = []
    for i in j_req:
        authors.append(i)
    return authors


def get_list_foregin_posts():
    req = requests.get('https://cmput-404-socialdistribution.herokuapp.com/service/allposts/', auth=('socialdistribution_t18','c404t18'), headers={'Referer': "http://127.0.0.1:9000/"})
    j_req = req.json()
    foregin_posts = j_req['posts']
    return foregin_posts