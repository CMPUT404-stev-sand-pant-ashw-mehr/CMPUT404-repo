from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.response import Response
from inbox.models import Inbox
from post.api import PostViewSet
from author.models import Author
from post.models import Post
from followers.models import FriendRequest
from likes.models import Like

class InboxViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET the inbox of the author
    def get_inbox(self, request, author_id=None):
        result, obj = self.check_author_exists(author_id)
        if not result:
            return obj
        author = obj
        if request.user != author.user:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        inboxItems = Inbox.objects.filter(author=author_id)
        if inboxItems.count == 0:
            return Response( {
                "type": "inbox",
                "author": self.get_author_uri(request),
                "items": []
            }, status=status.HTTP_200_OK)

        returnList = list()
        for items in inboxItems:
            if items["post_item_id"] != None:
                response = PostViewSet.get_post(self=PostViewSet, request=request, author_id=author_id, post_id=items["post_item_id"])
                if response.status_code != 200:
                    continue
                returnList.append(response.data)

            elif items["like_item_id"] != None:
                like_id = items["like_item_id"]
                try:
                    like = Like.objects.get(id=like_id)
                    like_data = dict()
                    like_data["@context"] = "https://www.w3.org/ns/activitystreams"
                    
                except:
                    continue
            
        

    #POST to add new item to the inbox of an author
    def post_inbox(self, request, author_id=None):
        pass

    def delete_inbox(self, request, author_id=None):
        pass

    
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
