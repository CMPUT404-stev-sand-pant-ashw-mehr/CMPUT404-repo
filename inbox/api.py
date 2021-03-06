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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @swagger_auto_schema(
        operation_description="GET /service/author/< AUTHOR_ID >/inbox",
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "type":"inbox",
                    "author":"http://127.0.0.1:5454/author/c1e3db8ccea4541a0f3d7e5c75feb3fb",
                    "items":[
                        {
                            "type":"post",
                            "title":"A Friendly post title about a post about web dev",
                            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                            "origin":"http://whereitcamefrom.com/posts/zzzzz",
                            "description":"This post discusses stuff -- brief",
                            "contentType":"text/plain",
                            "content":"???? w??s on burgum B??owulf Scyldinga, l??of l??od-cyning, longe ??r??ge folcum gefr??ge (f??der ellor hwearf, aldor of earde), o?? ????t him eft onw??c h??ah Healfdene; h??old ??enden lifde, gamol and g????-r??ow, gl??de Scyldingas. ????m f??ower bearn for??-ger??med in worold w??cun, weoroda r??swan, Heorog??r and Hr????g??r and H??lga til; hy??rde ic, ??at Elan cw??n Ongen????owes w??s Hea??oscilfinges heals-gebedde. ???? w??s Hr????g??re here-sp??d gyfen, w??ges weor??-mynd, ????t him his wine-m??gas georne hy??rdon, o?? ????t s??o geogo?? gew??ox, mago-driht micel. Him on m??d bearn, ????t heal-reced h??tan wolde, medo-??rn micel men gewyrcean, ??one yldo bearn ??fre gefr??non, and ????r on innan eall ged??lan geongum and ealdum, swylc him god sealde, b??ton folc-scare and feorum gumena. ???? ic w??de gefr??gn weorc gebannan manigre m??g??e geond ??isne middan-geard, folc-stede fr??twan. Him on fyrste gelomp ??dre mid yldum, ????t hit wear?? eal gearo, heal-??rna m??st; sc??p him Heort naman, s?? ??e his wordes geweald w??de h??fde. H?? b??ot ne ??l??h, b??agas d??lde, sinc ??t symle. Sele hl??fade h??ah and horn-g??ap: hea??o-wylma b??d, l????an l??ges; ne w??s hit lenge ???? g??n ????t se ecg-hete ????um-swerian 85 ??fter w??l-n????e w??cnan scolde. ???? se ellen-g??st earfo??l??ce ??r??ge ge??olode, s?? ??e in ??y??strum b??d, ????t h?? d??gora gehw??m dr??am gehy??rde hl??dne in healle; ????r w??s hearpan sw??g, swutol sang scopes. S??gde s?? ??e c????e frum-sceaft f??ra feorran reccan",
                            "author":{
                                "type":"author",
                                "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                "host":"http://127.0.0.1:5454/",
                                "displayName":"Lara Croft",
                                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                                "github": "http://github.com/laracroft",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                            },
                            "categories":["web","tutorial"],
                            "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                            "published":"2015-03-09T13:07:04+00:00",
                            "visibility":"FRIENDS",
                            "unlisted":False
                        },
                        {
                            "type": "Follow",      
                            "summary":"Greg wants to follow Lara",
                            "actor": {
                                "type" : "author",
                                "id": "http://127.0.0.1:8000/author/2",
                                "host": "http://127.0.0.1:8000/",
                                "displayName": "TestUser2",
                                "url": "http://127.0.0.1:8000/author/2",
                                "github": "https://github.com/testUser2",
                                "profileImage":"None"
                            },
                            "object": {
                                "type" : "author",
                                "id": "http://127.0.0.1:8000/author/1",
                                "host": "http://127.0.0.1:8000/",
                                "displayName": "TestUser1",
                                "url": "http://127.0.0.1:8000/author/1",
                                "github": "https://github.com/testUser1",
                                "profileImage":"None"
                            }
                        }
                    ]
                }
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "Author not found"},
                }
            ),
            "403": openapi.Response(
                description="Author not authorized",
                examples={
                    "application/json": {"detail": "Not authorized"},
                }
            ), 
        },
        tags=['Get Author Inbox'],
    )
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
    

    @swagger_auto_schema(
        operation_description="POST /service/author/< AUTHOR_ID >/inbox",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["type"]
        ),
        responses={
            "200": openapi.Response(
                description="OK",
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "Author not found"},
                }
            ),
            "403": openapi.Response(
                description="Author not authorized",
                examples={
                    "application/json": {"detail":"Not Authorized"}
                }
            ),
            "400": openapi.Response(
                description="Missing / Invalid POST data",
                examples={
                    "application/json": {"detail": "mssing field in json for 'post': {'source', 'contentType'}"},
                    "application/json": {"detail": "Invalid URL for '@context'"},
                    "application/json": {"detail": "field 'unlisted' can only be 'true' or 'false'. Current value: <value>"},
                    "application/json": {"detail": "'published' field datetime is not in ISO 8601 format"}
                }
            ), 
        },
        tags=['Add Inbox Items'],
    )
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



    @swagger_auto_schema(
        operation_description="DELETE /service/author/< AUTHOR_ID >/inbox",
        responses={
            "200": openapi.Response(
                description="OK"
            ),
            "204": openapi.Response (
                description="Already Empty"
            ),
            "404": openapi.Response(
                description="Author not found",
                examples={
                    "application/json": {"detail": "Author not found"},
                }
            ),
            "403": openapi.Response(
                description="Author not authorized",
                examples={
                    "application/json": {"detail":"Not Authorized"}
                }
            ),
        },
        tags=['Clear Inbox'],
    )
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

    #DELETE to clear the inbox
    def delete_from_inbox(self, request, author_id=None, foreign_id=None):
        result1, author= self.check_author_exists(author_id)
        result2, foreign_author = self.check_author_exists(foreign_id)

        if(result1 and result2):

            if request.user != author.user:
                return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

            items = list(Inbox.objects.filter(inbox_author_id=author_id).values())
            
            inbox = items[0]["items"]
            try:
                for i in range(len(inbox)):
                    item = inbox[i]
                    if(item['type']=="follow"):
                        temp = item['actor']['id'].split('/')
                        id=temp[len(temp)-1]
                        if id==foreign_id:
                            print(id)
                            update = inbox.copy()
                            update.pop(i)

                            new_items = Inbox.objects.get(inbox_author_id=author_id)
                            new_items.items = update.copy()
                            new_items.save()
                return Response({"message":"inbox updated"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "could not update"}, status=status.HTTP_404_NOT_FOUND)

    
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