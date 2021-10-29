from rest_framework.generics import get_object_or_404
from author.models import Author
from .serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response 
from django.http import HttpRequest
from rest_framework.response import Response
# from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from knox.auth import TokenAuthentication
from urllib.parse import urlparse

# Viewset for Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.exclude(user__isnull=True).order_by('id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorSerializer

    # GET all authors
    def list(self, request: HttpRequest):
        try:
            page = request.GET.get('page', 'None')
            size = request.GET.get('size', 'None')
            author_list = self.get_queryset()
            

            if(page == "None" or size == "None"):
                author_data = author_list.values()
            else:
                paginator = Paginator(author_list.values(), size)
                author_data = paginator.get_page(page).object_list

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
