from rest_framework.generics import get_object_or_404
from author.models import Author
from .serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, permissions, pagination
from rest_framework.decorators import action
from rest_framework.response import Response 
from django.http import HttpRequest
from rest_framework.response import Response
# from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from knox.auth import TokenAuthentication
from urllib.parse import urlparse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Viewset for Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.exclude(user__isnull=True).order_by('id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorSerializer

    @swagger_auto_schema(
        operation_description="GET /service/authors",
        manual_parameters=[
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="optional", 
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'size', 
                openapi.IN_QUERY, 
                description="optional", 
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":
                        {
                            "type": "authors",      
                            "items":[
                                        {
                                            "type":"author",
                                            "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                            "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                                            "host":"http://127.0.0.1:5454/",
                                            "displayName":"Greg Johnson",
                                            "github": "http://github.com/gjohnson",
                                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                        },
                                        {
                                            "type":"author",
                                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                            "host":"http://127.0.0.1:5454/",
                                            "displayName":"Lara Croft",
                                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                            "github": "http://github.com/laracroft",
                                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                                        }
                                ]
                        }
                }
                
            ),
            "400": openapi.Response(
                description="Bad Request",
                examples={
                    "application/json":{"message": "Error details..."}
                }
            )
        },
        tags=['Get all Authors'],
    )

    # GET all authors
    def list(self, request: HttpRequest):
        try:
            page = request.GET.get('page', 'None')
            size = request.GET.get('size', 'None')
            author_list = self.get_queryset()
            

            if(page == "None" or size == "None"):
                author_data = author_list.values()
            else:
                paginator = Paginator(author_list, size)
                author_data = paginator.get_page(page)

            for author in author_data:
                author["id"] = author["url"]

            response = {
                "type": "authors",
                "items": author_data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":{
                        "type":"author",
                        "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "host":"http://127.0.0.1:5454/",
                        "displayName":"Lara Croft",
                        "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        "github": "http://github.com/laracroft",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    }
                }
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "Author not found"}
                }
            ),
        },
        tags=['Get Author by Author ID'],
    )

    # GET using author id
    def get_author(self, request: HttpRequest, author_id=None):
        author_id = self.remove_backslash(author_id)
        try:
            print(self.get_queryset().values())
            query = self.get_queryset().get(id=author_id)
        except:
            return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        result = model_to_dict(query)
        result['id'] = result['url']
        return Response(result, status=status.HTTP_200_OK)

    # POST and update author's profile

    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["type", "id", "host", "url", "github", "profileImage"],
            properties={
                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                    "id": openapi.Schema(type=openapi.TYPE_STRING),
                    "host": openapi.Schema(type=openapi.TYPE_STRING),
                    "url": openapi.Schema(type=openapi.TYPE_STRING),
                    "github": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "profileImage": openapi.Schema(type=openapi.TYPE_STRING)
                },
        ),
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json":{
                        "message": "Record updated"
                    },
                     "application/json":{
                        "detail": "The following keys supplied are ignored: ..."
                     }
                }
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "Author not found"},
                }
            ),
            "400": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "No POST data is sent"},
                    "application/json": {
                        "message": "Record not updated",
                        "detail": "Error details..."}
                }
            ), 
        },
        tags=['Update Author by Author ID'],
    )

    def update(self, request: HttpRequest, author_id=None):
        author_id = self.remove_backslash(author_id)

        try:
            author = Author.objects.get(id=author_id)
        except:
            return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            ignored_keys = list()
            request_data = request.data.keys()

            if len(request_data) == 0:
                return Response({"detail": "No POST data is sent"}, status=status.HTTP_400_BAD_REQUEST)

            for key in request.data.keys():
                if(key == "displayName"):
                    author.displayName = request.data[key]

                elif(key == "github"):
                    author.github = request.data[key]

                elif(key == "profileImage"):
                    author.profileImage = request.data[key]
                else:
                    ignored_keys.append(key)

                author.save()
            if len(ignored_keys) == 0:
                response = {
                    "message": "Record updated"
                }
            else:
                response = {
                    "detail": "The following keys supplied are ignored: " + str(ignored_keys)
                }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            response = {
                "message": "Record not updated",
                "detail": e.args
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

    # validate if the url is the correct format
    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def remove_backslash(self, string: str) -> str:
        try:
            if string[-1] == '/':
                return string[:-1]
            else:
                return string
        except:
            return string
