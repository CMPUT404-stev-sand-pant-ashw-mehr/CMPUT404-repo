import json
import ast
from urllib.parse import urlparse
import re

from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from accounts.permissions import CustomAuthentication, AccessPermission
from rest_framework import viewsets, status
from rest_framework.response import Response
from author.serializer import AuthorSerializer
from inbox.serializers import InboxSerializer
from inbox.models import Inbox
from author.models import Author

class InboxViewSet(viewsets.ModelViewSet):
    serializer_class = InboxSerializer

    def initialize_request(self, request, *args, **kwargs):
     self.action = self.action_map.get(request.method.lower())
     return super().initialize_request(request, *args, kwargs)
    
    def get_authenticators(self):
        if self.action in ["post_inbox"]:
            return [CustomAuthentication()]
        else:
            return [TokenAuthentication()]
    
    def get_permissions(self):
        if self.action in ["post_inbox"]:
            return [AccessPermission()]
        else:
            return [IsAuthenticated()]


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

        response["author"] = author.url

        return Response(response, status=status.HTTP_200_OK)
            
    #POST to add new item to the inbox of an author
    def post_inbox(self, request, author_id=None):
        result, obj = self.check_author_exists(author_id)
        if not result:
            return obj

        try:
            itemType = request.data["type"]
            
            # Check if request data json is correct
            valid, error_message = self.validate_json(request.data, itemType.strip().lower())
            if not valid:
                return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

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
            author = Author.objects.exclude(is_active=False).get(id=author_id)
            return True, author
        except:
            return False, Response({"detail": "author not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_author_uri(self, request):
        uri = str(request.build_absolute_uri()).replace("/inbox", "")
        if (uri[-1] == '/'):
            uri = uri[:-1]
        return uri

    # Validate if the json stored to Inbox are in valid format
    def validate_json(self, input: dict, itemType: str):
        if itemType == "post":
            essiential_keys = {"type", "title", "id", "source", "origin", "description", "contentType", "content", "author", "categories", "visibility", "unlisted"}
        elif itemType == "like":
            essiential_keys = {"@context", "summary", "type", "author", "object"}
        elif itemType == "follow":
            essiential_keys = {"type", "summary", "actor", "object"}
        else:
            raise Exception(f"Unrecognized item type: {itemType}, must be in: ['post', 'like', 'follow']")

        missing_fields = set()
        if not essiential_keys.issubset(input.keys()):
            missing_fields = essiential_keys - input.keys()
            return False, f"mssing field in json for {itemType}: {missing_fields}"

        #detailed check

        if itemType == "post":
            # validate if these fields are valid url formats
            url_fields = {"id", "source", "origin", "comments"}
            for fk in url_fields:
                try:
                    if not self.validate_url(input[fk]):
                        return False, f"Invalid url for '{fk}' field"
                except KeyError:
                    continue

            # validate if author format is valid
            author_json = input["author"]
            try:
                if type(author_json) == dict:
                    author_dict = author_json
                else:
                    author_dict = json.loads(author_json)
            except json.JSONDecodeError as e:
                return False, "Invalid author JSON: " + e.msg

            author_validation = AuthorSerializer(data=author_dict)
            if not author_validation.is_valid():
                return False, f"invalid author field: {author_validation.error_messages}"

            # validate if categories is a list
            category_list = input["categories"]
            try:
                if type(category_list) != list:
                    ast.literal_eval(category_list)
            except Exception as e:
                return False, f"invalid cetegories list: {e}, Posted value: {category_list}"

            if not self.validate_date_format(input["published"]):
                return False, "'published' field datetime is not in ISO 8601 format"

            if input["visibility"] not in ["PUBLIC", "FRIENDS"]:
                return False, f"The key {input['visibility']} for field 'visibility' is invalid. 'visibility' must be either 'PUBLIC' or 'FRIENDS'"

            if str(input["unlisted"]).lower() not in ["true", "false"]:
                return False, f"field 'unlisted' can only be 'true' or 'false'. Current value: {input['unlisted']}"

        elif itemType == "like":
            if not self.validate_url(input["@context"]):
                return False, "Invalid URL for '@context'"

            if not self.validate_url(input["object"]):
                return False, "Invalid URL for 'object'"

            # validate if author format is valid
            author_json = input["author"]
            try:
                if type(author_json) == dict:
                    author_dict = author_json
                else:
                    author_dict = json.loads(author_json)
            except json.JSONDecodeError as e:
                return False, f"Invalid author JSON: " + e.msg

            author_validation = AuthorSerializer(data=author_dict)
            if not author_validation.is_valid():
                return False, f"invalid author field: {author_validation.error_messages}"

        elif itemType == "follow":
            author_validation_fields = {"actor", "object"}
            for f in author_validation_fields:
                author_json = input[f]
                try:
                    if type(author_json) == dict:
                        author_dict = author_json
                    else:
                        author_dict = json.loads(author_json)
                except json.JSONDecodeError as e:
                    return False, f"Invalid {f} JSON: {e.msg}"

                author_validation = AuthorSerializer(data=author_dict)
                if not author_validation.is_valid():
                    return False, f"invalid {f} field: {author_validation.error_messages}"

        return True, ""            
            
    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def validate_date_format(self, date: str):
        date_re = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

        match_iso = re.compile(date_re).match

        if match_iso(date):
            return True
        else:
            return False