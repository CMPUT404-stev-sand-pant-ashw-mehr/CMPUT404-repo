from django.forms.models import model_to_dict
from rest_framework.generics import get_object_or_404
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

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET a post with specified author id and post id
    def get_post(self, request, author_id=None, post_id=None):
        try:
            # get post with author.
            post_query = Post.objects.get(id=post_id, author=author_id)

            # get author. Exclude foreign author
            author_query = Author.objects.exclude(user__isnull=True).get(id=author_id)

        except:
            return Response({"detail": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        post_data = PostSerializer(data=post_query).data
        author_detail = model_to_dict(author_query)
        author_detail['id'] = author_detail['url']

        post_data['id'] = author_detail['id'] + '/posts/' + post_data['id']
        post_data['author'] = author_detail

        categories_query = Categories.objects.filter(post=post_id).values()
        categories = [c['category'] for c in categories_query]
        post_data['categories'] = categories

        post_data['comments'] = post_data['id'] + '/comments'

        comment_query = Comment.objects.filter(post=post_id, author=author_id).order_by('published')
        comment_details = Paginator(comment_query, 5) # get first 5 comments
        comment_serilaizer = CommentSerializer(comment_details.get_page(1), many=True)

        post_data["count"] = comment_query.distinct().count()

        post_data["CommentsSrc"] = {
            "type": "comments",
            "page": 1,
            "size": 5,
            "post": post_data["id"],
            "id": post_data["comments"],
            "comments": comment_serilaizer.data
        }

        return Response(post_data, status=status.HTTP_200_OK)

    def get_recent_post(self, request, author_id=None):
        pass

    # POST and update a post with given author_id and post_id
    def update_post(self, request, author_id=None, post_id=None):
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
        if request.method == "POST":
            post_id = uuid.uuid4
            get_object_or_404(Author, pk=author_id)




        elif request.method == "PUT":
            if not post_id:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete_post(self, request, author_id=None, post_id=None):
        try:
            post = Post.objects.get(author=author_id, id=post_id)
            post.delete()
            return Response({"detail": "Post deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)    