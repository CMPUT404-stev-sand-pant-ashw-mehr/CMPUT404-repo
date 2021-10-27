from author.models import Author
from .serializer import AuthorSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.decorators import action
from django.core.paginator import Paginator
from knox.auth import TokenAuthentication


# Viewset for Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.exclude(user__isnull=True)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorSerializer

    # GET all authors
    def list(self, request, *args, **kwargs):
        try:
            page = request.GET.get('page', 'None')
            size = request.GET.get('size', 'None')
            author_list = self.get_queryset()

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
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except:
            response = {
                "message": "Record not found"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    # POST
    def create(self, request, *args, **kwargs):
        try:
            new_author = Author(
                type=request.data["type"],
                id=request.data["id"],
                user=request.user,
                host=request.data["host"],
                displayName=request.data["displayName"],
                url=request.data["url"],
                github=request.data["github"],
                profileImage=request.data["profileImage"]
            )

            new_author.save()

            return Response(status.HTTP_201_CREATED)

        except Exception as e:
            response = {
                "message": "Record not created",
                "detail": e.args
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)


    # PUT
    def update(self, request, pk=None):
        try:
            for key in request.data.keys():
                author = Author.objects.get(id=pk)
                if(key=="url"):
                    author.url=request.data[key]

                elif(key=="host"):
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
