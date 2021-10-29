from django.forms.models import model_to_dict
from author.models import Author
from comment.models import Comment
from comment.serializers import CommentSerializer
from post.models import Post, Categories
from rest_framework import viewsets, status
from .serializers import PostSerializer
from rest_framework.response import Response 
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

import uuid
import ast

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET a post with specified author id and post id
    def get_post(self, request, author_id=None, post_id=None):
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]
            
        try:
            # get post with author.
            post_query = Post.objects.get(id=post_id, author=author_id, visibility="PUBLIC")

            # get author. Exclude foreign author
            author_query = Author.objects.exclude(user__isnull=True).get(id=author_id)

        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        post_data = model_to_dict(post_query)
        author_detail = model_to_dict(author_query)
        author_detail['id'] = author_detail['url']

        post_data['id'] = author_detail['id'] + '/posts/' + post_data['id']
        post_data['author'] = author_detail

        categories_query = Categories.objects.filter(post=post_id).values()
        categories = [c['category'] for c in categories_query]

        post_data['categories'] = categories

        post_data['comments'] = post_data['id'] + '/comments'

        comment_query = Comment.objects.filter(post=post_id, author=author_id).order_by('-published')
        comment_details = Paginator(comment_query.values(), 5) # get first 5 comments
        comment_object_list = comment_details.get_page(1).object_list.values()
        comment_serilaizer = CommentSerializer(data=[c for c in comment_object_list], many=True)

        if comment_serilaizer.is_valid():
            for entry in comment_serilaizer.data:
                entry['id'] = author_detail['url'] + '/posts/' + post_id + '/comments/' + entry['id']

            post_data["count"] = comment_query.distinct().count()

            if post_data["count"] > 0:
                post_data["CommentsSrc"] = {
                    "type": "comments",
                    "page": 1,
                    "size": 5,
                    "post": post_data["id"],
                    "id": post_data["comments"],
                    "comments": comment_serilaizer.data
                }
            else:
                post_data["CommentsSrc"] = dict()

            return Response(post_data, status=status.HTTP_200_OK)
        else:
            return Response(comment_serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET recent post
    def get_recent_post(self, request, author_id=None):
        posts_query = Post.objects.filter(author=author_id, visibility="PUBLIC", unlisted=False)
        if not posts_query.exists():
            return Response({"detail": "Author not found or does not have public posts"}, status=status.HTTP_404_NOT_FOUND)
        
        # Order by recent
        posts_query = posts_query.order_by('-published')

        page = request.GET.get('page', 'None')
        size = request.GET.get('size', 'None')

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
            author_detail = model_to_dict(Author.objects.get(id=author_id))
            author_detail['id'] = author_detail['url']

            post_data['id'] = author_detail['id'] + '/posts/' + post_data['id']
            post_data['author'] = author_detail

            categories_query = Categories.objects.filter(post=post_id).values()
            categories = [c['category'] for c in categories_query]

            post_data['categories'] = categories

            post_data['comments'] = post_data['id'] + '/comments'

            comment_query = Comment.objects.filter(post=post_id, author=author_id).order_by('-published')
            comment_details = Paginator(comment_query.values(), 5) # get first 5 comments
            comment_object_list = comment_details.get_page(1).object_list.values()
            comment_serilaizer = CommentSerializer(data=[c for c in comment_object_list], many=True)

            if comment_serilaizer.is_valid():
                for entry in comment_serilaizer.data:
                    entry['id'] = author_detail['url'] + '/posts/' + post_id + '/comments/' + entry['id']

                post_data["count"] = comment_query.distinct().count()

                if post_data["count"] > 0:
                    post_data["CommentsSrc"] = {
                        "type": "comments",
                        "page": 1,
                        "size": 5,
                        "post": post_data["id"],
                        "id": post_data["comments"],
                        "comments": comment_serilaizer.data
                    }
                else:
                    post_data["CommentsSrc"] = dict()

                return_list.append(post_data)

            else:
                return Response(comment_serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "type": "posts",
            "page": page,
            "size": size,
            "id": request.build_absolute_uri(),
            "items": return_list,
        }, status=status.HTTP_200_OK)


    # POST and update a post with given author_id and post_id
    def update_post(self, request, author_id=None, post_id=None):
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]
        try:
            author = Author.objects.get(id=author_id)
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
                        return Response({"detail": "Invalid visibility key"}, status=status.status.HTTP_400_BAD_REQUEST)
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
        
    # POST to create a post with generated post_id, PUT to put a post with specified post id
    def create_post(self, request, author_id=None, post_id=None):
        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if request.method == "POST":
            post_id = str(uuid.uuid4().hex)

            try:
                request_keys = request.data

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

                visi = request_keys['visibility'].strip()
                if (visi not in ("PUBLIC", "FRIENDS")):
                    return Response({"detail": "Invalid visibility key"}, status=status.status.HTTP_400_BAD_REQUEST)
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
                        categories = ast.literal_eval(str(categories))
                    except:
                        return Response({"detail": "incorrect format for Categories"}, status=status.HTTP_400_BAD_REQUEST)

                    for label in categories:
                        Categories.objects.create(post_id=post_id, category=label)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except KeyError as e:
                return Response({"detail": "key(s) missing:", "message": e.args}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "PUT":
            if not post_id:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            # remove trailing slash
            if post_id[-1] == '/':
                post_id = post_id[:-1]
            
            #TODO
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
            
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete_post(self, request, author_id=None, post_id=None):
        # remove trailing slash
        if post_id[-1] == '/':
            post_id = post_id[:-1]

        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if author.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            post = Post.objects.get(author=author_id, id=post_id)
            post.delete()
            return Response({"detail": "Post deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": e.args}, status=status.HTTP_404_NOT_FOUND)    