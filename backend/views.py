# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework import status
from .models import Post, Comment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


class ListPosts(APIView):
    """
    View to list all public posts(assuming all posts are public for the time) in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="GET /post/",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "total": 2,
                        "post": [
                            {
                                "author": "Author A",
                                "data_type": "jpeg",
                                "data": "linktoanimage"
                            },
                            {
                                "author": "Author B",
                                "data_type": "text",
                                "data": "Sample string in the post"
                            }
                        ]
                    }
                }
            )
        },
        tags=['Get all posts'],
    )

    def get(self, request):
        """
        Return a list of all posts
        """
        posts = Post.objects.all()

        post_list = []

        for post in posts:
            post_obj = {
                    "author": post.author,
                    "data_type": post.data_type,
                    "data": post.data,
            }
            post_list.append(post_obj)

        total = len(posts)
            
        response = {
            "total" : total,
            "books" : post_list
        }
        
        return Response(response, status=status.HTTP_200_OK)

