import io
from rest_framework.parsers import JSONParser
from django.forms.models import model_to_dict
from author.models import Author
from author.serializer import AuthorSerializer
from comment.models import Comment
from post.models import Post, Categories
from likes.models import Like
from rest_framework import viewsets, status
from .serializers import PostSerializer
from likes.serializers import LikeSerializer
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.permissions import CustomAuthentication, AccessPermission
from accounts.helper import  is_valid_node

import uuid
import ast

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    def initialize_request(self, request, *args, **kwargs):
     self.action = self.action_map.get(request.method.lower())
     return super().initialize_request(request, *args, kwargs)
    
    def get_authenticators(self):
        if self.action in ["get_post", "get_public_posts", "get_recent_post"]:
            return [CustomAuthentication()]
        else:
            return [TokenAuthentication()]
    
    def get_permissions(self):
        if self.action in ["get_post", "get_public_posts", "get_recent_post"]:
            return [AccessPermission()]
        else:
            return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/posts/< POST_ID >",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {
                        "type":"post",
                        "title":"A post title about a post about web dev",
                        "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                        "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                        "origin":"http://whereitcamefrom.com/posts/zzzzz",
                        "description":"This post discusses stuff -- brief",
                        "contentType":"text/plain",
                        "content":"Test Content",
                        "author":{
                            "type":"author",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Lara Croft",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github": "http://github.com/laracroft",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        },
                        "categories":["web","tutorial"],
                        "count": 1023,
                        "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                        "commentsSrc":{
                            "type":"comments",
                            "page":1,
                            "size":5,
                            "post":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                            "comments":[
                                {
                                    "type":"comment",
                                    "author":{
                                        "type":"author",
                                        "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                        "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                        "host":"http://127.0.0.1:5454/",
                                        "displayName":"Greg Johnson",
                                        "github": "http://github.com/gjohnson",
                                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                    },
                                    "comment":"Sick Olde English",
                                    "contentType":"text/markdown",
                                    "published":"2015-03-09T13:07:04+00:00",
                                    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                                }
                            ]
                        },
                        "published":"2015-03-09T13:07:04+00:00",
                        "visibility":"PUBLIC",
                        "unlisted":"false"
                   }
                }
            ),
            "403": openapi.Response(
                description="Node not allowed",
                examples= {
                    "application/json": {"detail":"Node not allowed"}, 
                }
            ),
            "404": openapi.Response(
                description="Post not found",
                examples={
                    "application/json":{"detail": "post not found"}
                }
            ),
        },
        tags=['Get an Author\'s Post'],
    )
    # GET a post with specified author id and post id
    def get_post(self, request, author_id=None, post_id=None) -> Response:
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]
            
        try:
            # get post with author.
            post_query = Post.objects.get(id=post_id, author=author_id)

            # get author. Exclude foreign author
            author_query = Author.objects.exclude(is_active=False).exclude(user__isnull=True).get(id=author_id)

        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        post_data = model_to_dict(post_query)
        author_detail = AuthorSerializer(author_query).data

        post_data['id'] = author_detail['id'] + '/posts/' + post_data['id']
        post_data['author'] = author_detail

        categories_query = Categories.objects.filter(post=post_id).values()
        categories = [c['category'] for c in categories_query]

        post_data['categories'] = categories

        post_data['comments'] = post_data['id'] + '/comments'

        comment_query = Comment.objects.filter(post_id=post_id, author_id=author_id).order_by('-published')
        comment_details = Paginator(comment_query.values(), 5) # get first 5 comments
        comment_object_list = comment_details.get_page(1).object_list.values()

        comment_list = list()
        for entry in comment_object_list:
            comment_author_id = entry.pop('author_id', None)
            author_details = model_to_dict(Author.objects.get(id=comment_author_id))
            author_details['id'] = author_details['url']
            entry['author'] = author_details
            entry['id'] = author_detail['url'] + '/posts/' + post_id + '/comments/' + entry['id']
            comment_list.append(entry)

        post_data["count"] = comment_query.distinct().count()

        if comment_query.distinct().count() > 0:
            post_data["commentsSrc"] = {
                "type": "comments",
                "page": 1,
                "size": 5,
                "post": post_data["id"],
                "id": post_data["comments"],
                "comments": comment_list
            }
        else:
            post_data["commentsSrc"] = dict()

        return Response(post_data, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        operation_description="GET /service/posts/",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {
                        "type": "posts",
                        "page": "5",
                        "size": "2",
                        "id": "http://127.0.0.1:8000/author/46527adf186c48a993bab65ed54c26e2/posts",
                        "items": "[Post Object 1, Post Object 2]",
                    }
                }
            ),
            "403": openapi.Response(
                description="Node not allowed",
                examples= {
                    "application/json": {"detail":"Node not allowed"}, 
                }
            ),
        }
    )
    # GET all public posts on this server
    def get_public_posts(self, request):
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)

        post_set = Post.objects.filter(visibility="PUBLIC", unlisted=False)
        
        return Response(self.get_post_from_query(posts_query=post_set, request=request), status=status.HTTP_200_OK)
            
    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/posts/",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {
                        "type": "posts",
                        "page": "5",
                        "size": "2",
                        "id": "http://127.0.0.1:8000/author/46527adf186c48a993bab65ed54c26e2/posts",
                        "items": "[Post Object 1, Post Object 2]",
                    }
                }
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json":{"detail": "author not found"}
                }
            ),
            "400": openapi.Response(
                description="Bad request",
            ),
        },
        tags=['Get an Author\'s Recent Posts'],
    )
    # GET recent post
    def get_recent_post(self, request, author_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            author = Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

        posts_query = Post.objects.filter(author=author)
        
        return Response(self.get_post_from_query(posts_query=posts_query, request=request), status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="PUT service/author/< AUTHOR_ID >/posts/< POST_ID >",
        request_body=openapi.Schema(    
            type=openapi.TYPE_OBJECT,
            properties={
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                    },
        ),
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"message": "Record updated"},
                   "application/json":  {
                        "message": "Record not updated",
                        "detail": "Error details"
                    }
                }
            ),
            "403": openapi.Response(
                description="Node or Author not allowed",
                examples= {
                    "application/json": {"detail":"Node not allowed"}, 
                    "application/json": {"detail": "author not allowed"}
                }
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json":{"detail": "author not found"},
                    "application/json":{"detail": "post not found"}
                }
            ),
            "400": openapi.Response(
                description="Bad request",
                examples={
                    "application/json":{"detail": "No POST data is sent"},
                    "application/json":{"detail": "Invalid visibility key"}
                }
            ),
        },
        tags=['Update an Author\'s Post'],
    )
    # POST and update a post with given author_id and post_id
    def update_post(self, request, author_id=None, post_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"detail":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]
        try:
            author = Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        try:
            post = Post.objects.get(author=author_id, id=post_id)
        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        try:            
            ignored_keys = list()
            request_data = request.data.keys()
            
            if len(request_data) == 0:
                return Response({"detail": "No POST data is sent"}, status=status.HTTP_400_BAD_REQUEST)

            for key in request.data.keys():
                if(key=="title"):
                    post.title = request.data[key]

                elif(key=="description"):
                    post.description = request.data[key]

                elif(key=="content"):
                    post.content = request.data[key]

                elif(key=="visibility"):
                    visi = request.data[key].strip()
                    if (visi not in ("PUBLIC", "FRIENDS")):
                        return Response({"detail": "Invalid visibility key"}, status=status.HTTP_400_BAD_REQUEST)
                    post.visibility = visi

                else:
                    ignored_keys.append(key)

                post.save()

            if len(ignored_keys) == 0:
                response={
                    "message": "Record updated"
                }
            else:
                response={
                    "detail": "The following keys supplied are ignored: " + str(ignored_keys)
                }
            return Response(response,status.HTTP_200_OK)
        except Exception as e:
            response={
                "message": "Record not updated",
                "detail": e.args
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/posts/\r\nPUT /service/author/< AUTHOR_ID >/posts/< POST_ID >",
        request_body=openapi.Schema(    
            type=openapi.TYPE_OBJECT,
            required=["type", "id", "title", "source", "origin", "author", "description", "contentType", "content", "published", "visibility", "unlisted"],
            properties=
                {
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                    'title': openapi.Schema(type=openapi.TYPE_STRING), 
                    'source': openapi.Schema(type=openapi.TYPE_STRING), 
                    'origin': openapi.Schema(type=openapi.TYPE_STRING), 
                    'author': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING), 
                    'contentType': openapi.Schema(type=openapi.TYPE_STRING),
                    'content': openapi.Schema(type=openapi.TYPE_STRING),
                    'published': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'visibility': openapi.Schema(type=openapi.TYPE_STRING),
                    'unlisted': openapi.Schema(type=openapi.TYPE_BOOLEAN),  
                },
        ),
        responses={
            "201": openapi.Response(
                description="Created",
            ),
            "400": openapi.Response(
                description="Bad Request",
                examples={
                    "application/json":{"detail": "Invalid visibility key"},
                    "application/json":{"detail": "unlisted must be boolean"},
                    "application/json":{"detail": "incorrect format for Categories"},
                }
            ),
            "404": openapi.Response(
                description="Not Found",
                examples={
                    "application/json":{"detail": "Author not found"},
                }
            ),
            
            "403": openapi.Response(
                description="Node or Author not allowed",
                examples= {
                    "application/json": {"detail":"Node not allowed"}, 
                    "application/json": {"detail": "author not allowed"}
                }
            ),
            "405": openapi.Response(
                description="Method not Allowed"
            )
        },
        tags=['Create an Author\'s Post'],
    )
        
    # POST to create a post with generated post_id, PUT to put a post with specified post id
    def create_post(self, request, author_id=None, post_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"detail":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response({"detail": "author not allowed"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == "POST":
            post_id = str(uuid.uuid4().hex)
            request_keys = request.data.copy()
            request_keys['source'] = request.build_absolute_uri('/')
            request_keys['origin'] = request.build_absolute_uri('/')
        elif request.method == "PUT":
            if not post_id:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

            # remove trailing slash
            if post_id[-1] == '/':
                post_id = post_id[:-1]

            try:
                stream = io.BytesIO(request.body)
                request_keys = JSONParser().parse(stream)
            except Exception as e:
                return Response({"detail": f"Cannot parsing PUT body: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            data = dict()
            data['type'] = request_keys['type']
            data['title'] = request_keys['title']
            data['id'] = post_id
            data['source'] = request_keys['source']
            data['origin'] = request_keys['origin']
            data['description'] = request_keys['description']
            data['contentType'] = request_keys['contentType']
            data['content'] = request_keys['content']
            data['author'] = author_id

            try:
                visi = request_keys['visibility'].strip()
            except AttributeError:
                return Response({"detail": f"'visibility' key must be a string, either 'PUBLIC' or FRIENDS. Request value: {request_keys['visibility']}"}, status=status.HTTP_400_BAD_REQUEST)
            if (visi not in ("PUBLIC", "FRIENDS")):
                return Response({"detail": "Invalid visibility key"}, status=status.HTTP_400_BAD_REQUEST)
            data['visibility'] = visi

            unlisted = str(request_keys['unlisted']).strip().lower()
            if unlisted not in ["false", "true"]:
                return Response({"detail": "unlisted must be boolean"}, status=status.HTTP_400_BAD_REQUEST)
            elif unlisted == 'false':
                data['unlisted'] = False
            else:
                data['unlisted'] = True
            
            serializer = PostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                categories = request_keys['categories']

                try:
                    if type(categories)!= list:
                        categories = ast.literal_eval(str(categories))
                    #check if it is iterable
                    iter(categories)
                except:
                    return Response({"detail": "incorrect format for Categories"}, status=status.HTTP_400_BAD_REQUEST)

                for label in categories:
                    Categories.objects.create(post_id=post_id, category=label)

                return_data = serializer.data
                return_data['author'] = AuthorSerializer(author).data
                return Response(return_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            return Response({"detail": "key(s) missing: " + e.args}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="DELETE /service/author/< AUTHOR_ID >/posts/< POST_ID >",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                   "application/json": {"detail": "Post deleted"}
                }
            ),
            "403": openapi.Response(
                description="Node or Author not allowed",
                examples= {
                    "application/json": {"detail":"Node not allowed"}, 
                    "application/json": {"detail": "author not allowed"}

                }
            ),
            "404": openapi.Response(
                description="Post or Author not found",
                examples={
                    "application/json":{"detail": "Post not found"},
                    "application/json": {"detail": "author not found"}
                }
            ),
        },
        tags=['Delete an Author\'s Post'],
    )
    
    def delete_post(self, request, author_id=None, post_id=None):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"detail":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]

        try:
            author = Author.objects.exclude(is_active=False).get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response({"detail": "author not allowed"}, status=status.HTTP_403_FORBIDDEN)

        try:
            post = Post.objects.get(author=author_id, id=post_id)
            post.delete()
            return Response({"detail": "Post deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": e.args}, status=status.HTTP_404_NOT_FOUND)    


    def get_post_from_query(self, request, posts_query) -> dict():
        # Order by recent
        posts_query = posts_query.order_by('-published')

        page = request.GET.get('page', "1")
        size = request.GET.get('size', "5")

        if(page == "None" or size == "None"):
            post_data_list = posts_query.values()
        else:
            paginator = Paginator(posts_query.values(), size)
            post_data_list = paginator.get_page(page).object_list

        return_list = list()

        for post_data in post_data_list:
            # This is the same as the get_post
            # Should've made it in the serializer but too late to figure that out
            author_id = post_data['author_id']
            post_id = post_data['id']
            author_detail = AuthorSerializer(Author.objects.get(id=author_id)).data

            post_data['id'] = author_detail['url'] + '/posts/' + post_data['id']
            post_data['author'] = author_detail

            categories_query = Categories.objects.filter(post=post_id).values()
            categories = [c['category'] for c in categories_query]

            post_data['categories'] = categories

            like_query = Like.objects.filter(post=Post.objects.get(id=post_id))
            like_res = LikeSerializer(like_query, many=True).data
            
            for likeObj in like_res:
                likeObj['@context'] = "https://www.w3.org/ns/activitystreams"
                likeObj['author'] = AuthorSerializer(Author.objects.get(id=likeObj["author"])).data
                name = likeObj['author']["displayName"]
                
            post_data["likes"] = like_res

            post_data['comments'] = post_data['id'] + '/comments'

            comment_query = Comment.objects.filter(post=post_id, author=author_id).order_by('-published')
            comment_details = Paginator(comment_query.values(), 5) # get first 5 comments
            comment_object_list = comment_details.get_page(1).object_list.values()

            comment_list = list()
            for entry in comment_object_list:
                comment_author_id = entry.pop('author_id', None)
                author_details = AuthorSerializer(Author.objects.get(id=comment_author_id)).data
                author_details['id'] = author_details['url']
                entry['author'] = author_details
                entry['id'] = author_detail['url'] + '/posts/' + post_id + '/comments/' + entry['id']
                comment_list.append(entry)

            post_data["count"] = comment_query.distinct().count()

            if post_data["count"] > 0:
                post_data["commentsSrc"] = {
                    "type": "comments",
                    "page": 1,
                    "size": 5,
                    "post": post_data["id"],
                    "id": post_data["comments"],
                    "comments": comment_list
                }
            else:
                post_data["commentsSrc"] = dict()
            return_list.append(post_data)   

        next = None
        previous = None
        if(page != "None"):
            next = ((int(page) + 1)) if Paginator(posts_query.values(), size).get_page(page).has_next() else None 
            previous = ((int(page) - 1)) if Paginator(posts_query.values(), size).get_page(page).has_previous() else None

        return {
            "type": "posts",
            "page": page,
            "size": size,
            "id": request.build_absolute_uri(),
            "items": return_list,
            "next": next, 
            "previous": previous
        }