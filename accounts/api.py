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





# IDK WHAT THIS IS FOR
class ProfileAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user 
