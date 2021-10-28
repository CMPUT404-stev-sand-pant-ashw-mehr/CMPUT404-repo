from rest_framework import generics, permissions, status, validators
from rest_framework.response import Response 
from knox.models import AuthToken
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from author.models import Author
from author.serializer import AuthorSerializer
from django.contrib.auth.models import User

from knox.models import AuthToken

import json


class RegisterAPI(generics.GenericAPIView):
    """
    User & Author Registration
    """
    serializer_class = RegisterSerializer

    def post(self, request):

        user_serializer = self.get_serializer(data = request.data)
        user_serializer.is_valid(raise_exception = True)
        # create user
        user = user_serializer.save()


        token = AuthToken.objects.create(user=user)

        author_schema = {
            "host" : "",
            "displayName": request.data["displayName"],
            "github": request.data["github"],
            "user": user.id
        }

        author_serialized_data = AuthorSerializer(data = author_schema)

        if not (author_serialized_data .is_valid()):
            user.delete()
            raise validators.ValidationError(author_serialized_data .errors)

        author =  author_serialized_data.save(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'author': AuthorSerializer(author).data,
            'token': 'Token ' + token[1]
        }, status=status.HTTP_201_CREATED)



        # Create an author object

        # if request.data.get('github', False):
        #     author = Author(
        #         user=user,
        #         token=token,
        #         host =request.data["host"],
        #         displayName=request.data["displayName"],
        #         github=request.data["github"],
        #         profileImage=request.data["profileImage"],
        #     )
        #     # this might not work if github does not match display
        # else:
        #     author = Author(
        #         user=user,
        #         token=token,
        #         host=request.data["host"],
        #         displayName=request.data["displayName"],
        #         github="https://github.com/" + request.data["displayName"],
        #         profileImage=request.data["profileImage"],
        #     )
        # # URL of author is generated on creation
        # author_serializer = AuthorSerializer(data=author)

        # if not (author_serializer.is_valid()):
        #     user.delete()
        #     raise validators.ValidationError(author_serializer.errors)
        

        # response = "Successfully Registered!"

        # return Response(response, status=status.HTTP_201_created)


class LoginAPI(generics.GenericAPIView):
    '''
    Takes username & password to autheticate the user
    '''
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.select_related('author').get(username=username)

        token = AuthToken.objects.create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'author': AuthorSerializer(user.author).data,
            'token': 'Token ' + token[1]
        }, status=status.HTTP_200_OK)


    # queryset = Author.objects.all()

    # permission_classes = [
    #     permissions.AllowAny
    # ]

    # serializer_class = Login
    # def post(self, request):
    #     serializer = self.get_serializer(data = request.data)
    #     serializer.is_valid(raise_exception = True)
    #     user = serializer.validated_data["username"]

    #     token = AuthToken.objects.create(user)[1]

    #     return Response({
    #         "user": UserSerializer(user, context = self.get_serializer_context()).data,
    #         "token": token
    #     })




# IDK WHAT THIS IS FOR
class ProfileAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user 
