from rest_framework import generics, permissions, status, validators
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response 
from knox.models import AuthToken
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from author.serializer import AuthorSerializer
from django.contrib.auth.models import User
from author.models import Author
from knox.models import AuthToken
from .helper import get_list_foregin_authors, get_list_foregin_posts, is_valid_node
from author.models import Author
from .permissions import AccessPermission, CustomAuthentication
from drf_yasg.utils import swagger_auto_schema

import uuid

@swagger_auto_schema(
    tags=['Register an author'],
)
class RegisterAPI(generics.GenericAPIView):
    """
    User & Author Registration
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        host = 'http://' + str(request.get_host())
        user_serializer = self.get_serializer(data = request.data)
        user_serializer.is_valid(raise_exception=True)
        # create user
        user = user_serializer.save()

        author_uuid = uuid.uuid4().hex

        author_schema = {
            "host" : host,
            "id": str(author_uuid),
            "url": host + '/author/' + str(author_uuid),
            "displayName": request.data["displayName"],
            "github": request.data["github"],
            "user": user.id
        }

        author_serialized_data = AuthorSerializer(data = author_schema)

        if not (author_serialized_data.is_valid()):
            user.delete()
            raise validators.ValidationError(author_serialized_data.errors)

        author =  author_serialized_data.save(user=user)

        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    tags=['Author login with username and password'],
)
class LoginAPI(generics.GenericAPIView):
    '''
    Takes username & password to autheticate the user
    '''
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        # node check
        valid = is_valid_node(request)
        if not valid:
            return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.select_related('author').get(username=username)
        try:
            get_object_or_404(Author, id=user.author.id, is_active=True)
        except:
            return Response({
                "message": "Unauthorized User"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'user': UserSerializer(user).data,
            'author': AuthorSerializer(user.author).data,
            'token': AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)

@swagger_auto_schema(
    tags=["Get all authors' profiels"],
)
class ProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user 



@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_authors(request):
    if request.method == "GET":
        foreign_authors = get_list_foregin_authors()
        print(foreign_authors)
        return Response({"foregin authors": foreign_authors})
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_foregin_posts(request):
    if request.method == "GET":
        foreign_posts = get_list_foregin_posts()
        print(foreign_posts)
        return Response({"foregin posts": foreign_posts})
    else:
        return Response({"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)