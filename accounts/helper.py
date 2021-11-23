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

def get_list_ids():
    req = requests.get('https://otherteam.herokuapp.com/service/authors/', auth=('',''), headers={'Referer': "https://social-dis.herokuapp.com/"}).json()
    ids = []
    authors = req["items"]
    for i in authors:
        ids.append(i["id"])
    return ids

def find_remote_author_by_id(id):
    req = requests.get('https://otherteam.herokuapp.com/service/author/'+id+'/', auth=('',''), headers={'Referer': "https://social-dis.herokuapp.com/"}).json()
    return req