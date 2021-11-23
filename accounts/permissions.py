from rest_framework import authentication, permissions
from knox.auth import TokenAuthentication
import base64

class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print("worked1")
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialdistribution_t03:c404t03').decode()
        if token_type == 'Basic' and credentials == expected:
            return True
        elif token_type == 'Token':
            return permissions.IsAuthenticated().has_permission(request=request, view=view)
        else:
            return False

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print("worked2")
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialdistribution_t03:c404t03').decode()
        if token_type == 'Basic' and credentials == expected:
            return (True, None)
        elif token_type == 'Token':
            return TokenAuthentication().authenticate(request=request)
        else:
            return None

    def authenticate_header(self, request):
        return '{"username" : <username>, "password" : <password>}'