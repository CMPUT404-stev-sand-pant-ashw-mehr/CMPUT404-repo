from rest_framework.generics import get_object_or_404
from author.models import Author
from .serializer import AuthorSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.http import HttpRequest
from rest_framework.response import Response
# from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.db.models import F
from knox.auth import TokenAuthentication
from urllib.parse import urlparse

# Viewset for Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.exclude(user__isnull=True)
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)

    serializer_class = AuthorSerializer

    # GET all authors
    def list(self, request: HttpRequest):
        try:
            page = request.GET.get('page', 'None')
            size = request.GET.get('size', 'None')
            author_list = self.get_queryset()

            # Swap the id fields to url
            author_list.update(id=F('url'))

            if(page == "None" or size == "None"):
                serializer = AuthorSerializer(author_list, many=True)
            else:
                paginator = Paginator(author_list, size)
                result_page = paginator.get_page(page)
                serializer = AuthorSerializer(result_page, many=True)

            response = {
                "type": "authors",
                "items": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                "message": "Records not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    # GET using author id
    def get_author(self, request: HttpRequest, author_id=None):
        query = self.get_queryset().filter(id=author_id)

        if not query.exists():
            return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        query.update(id=F('url'))

        return Response(query.values(), status=status.HTTP_200_OK)


    # POST and update author's profile
    def update(self, request: HttpRequest, author_id=None):
        try:
            author = Author.objects.get(id=author_id)
            if not author.exists():
                return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
                
            for key in request.data.keys():
                if(key=="url"):
                    if not self.validate_url(request.data[key]):
                        return Response({"detail": "url format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
                    author.url=request.data[key]

                elif(key=="host"):
                    if not self.validate_url(request.data[key]):
                        return Response({"detail": "host format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
                    author.host=request.data[key]

                elif(key=="displayName"):
                    author.displayName=request.data[key]

                elif(key=="github"):
                    author.github=request.data[key]

                elif(key=="profileImage"):
                    author.profileImage=request.data[key]

                author.save()

            response={
                "message": "Record updated"
            }
            return Response(response,status.HTTP_200_OK)
        except:
            response={
                "message": "Record not updated",
                "detail": "Incorrect data keys"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)

    # validate if the url is the correct format
    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
