from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.response import Response
from inbox.serializers import InboxSerializer
from inbox.models import Inbox
from author.models import Author

class InboxViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InboxSerializer

    # GET the inbox of the author
    def get_inbox(self, request, author_id=None):
        result, obj = self.check_author_exists(author_id)
        if not result:
            return obj
        author = obj

        if request.user != author.user:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        inboxItems, _ = Inbox.objects.get_or_create(inbox_author_id=author_id)

        response = InboxSerializer(inboxItems).data

        if len(response) > 0:
            response["author"] = self.get_author_uri(request)

        return Response(response, status=status.HTTP_200_OK)
            
    #POST to add new item to the inbox of an author
    def post_inbox(self, request, author_id=None):
        result, obj = self.check_author_exists(author_id)
        if not result:
            return obj

        try:
            itemType = request.data["type"]
            if type(itemType) != str or itemType.strip().lower() not in ["post", "like", "follow"]:
                return Response({"detail": f"item type '{itemType}' not in 'post', 'Like' or 'Follow'"}, status = status.HTTP_400_BAD_REQUEST)

            inbox, _ = Inbox.objects.get_or_create(inbox_author_id=author_id)
            inbox.items.insert(0, request.data)
            inbox.save()
            return Response(InboxSerializer(inbox).data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"detail": f"Missing field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": e.args}, status=status.HTTP_400_BAD_REQUEST)

    #DELETE to clear the inbox
    def delete_inbox(self, request, author_id=None):
        result, obj = self.check_author_exists(author_id)
        if not result:
            return obj
        author = obj

        if request.user != author.user:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        items = Inbox.objects.filter(inbox_author_id=author_id)

        if items.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            items.delete()
            return Response(list(items.values()), status=status.HTTP_200_OK)
    
    def check_author_exists(self, author_id=None):
        # Check if an author exist given the author id. If it is, return the author. If not, return 404 Response
        try:
            author = Author.objects.get(id=author_id)
            return True, author
        except:
            return False, Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_author_uri(self, request):
        uri = str(request.build_absolute_uri()).replace("/inbox", "")
        if (uri[-1] == '/'):
            uri = uri[:-1]
        return uri
