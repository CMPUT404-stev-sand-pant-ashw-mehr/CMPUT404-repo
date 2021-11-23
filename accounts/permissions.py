from rest_framework import authentication, permissions
import base64

class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print("worked1")
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialdistribution_t03:c404t03').decode()
        if token_type == 'Basic' and credentials == expected:
            return True
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
        else:
            return None

    def authenticate_header(self, request):
        return '{"username" : <username>, "password" : <password>}'