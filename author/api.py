from author.models import Author 
from rest_framework import viewsets, permissions 
from .serializer import AuthorSerializer 
from rest_framework.response import Response
from rest_framework import status

# Viewset for Author
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AuthorSerializer

    # GET all authors
    def list(self, request, *args, **kwargs):
        try:
            author_list = self.get_queryset()
            serializer = AuthorSerializer(author_list, many=True)
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
            return super().create(request, *args, **kwargs)
        except:
            response = {
                "message": "Record not created"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)


    # PUT
    def update(self, request, pk=None):
        print(request.data)
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
                "message": "Record not updated"
            }
            return Response(response,status.HTTP_400_BAD_REQUEST)
