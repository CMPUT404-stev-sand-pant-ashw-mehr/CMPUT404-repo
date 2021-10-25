from django.http.response import HttpResponse, HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from followers.serializers import FollowerModelSerializer
from author.serializer import AuthorSerializer
from followers.models import Followers
from django.contrib.auth.models import User

import io
import json
from rest_framework.parsers import JSONParser

import requests

class FollowerViewSet(viewsets.ModelViewSet):

    # GET list of followers
    def list(self, request, author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        follower_rows = Followers.objects.filter(author_id=author_id).values()
        # check if follower_rows is empty
        if not len(follower_rows):
            return HttpResponse({
                "type": "followers",
                "items":{}
            }, content_type='application/json')
        
        follower_items = list()

        for follower in follower_rows:
            f_url = str(follower["follower_url"])

            follower_details = requests.get(f_url)
            if follower_details.status_code == 200:
                serializer = AuthorSerializer(follower_details.json())
                if serializer.is_valid():
                    follower_items.append(serializer.data)
                else:
                    print(serializer.errors)

        return HttpResponse({
                "type": "followers",
                "items": str(follower_items)
            }, content_type='application/json')

    def put_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

        try:
            content_type = request.META["CONTENT_TYPE"]

            if content_type != "application/json":
                raise HttpResponseBadRequest(json.dumps({"detail": "invalid content type. Required: application/json"}), content_type="application/json")

            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            serializer = AuthorSerializer(data=data)

            if not serializer.is_valid():
                return HttpResponseBadRequest(json.dumps({"detail": "Invalid json format for author", "errors": serializer.errors}), content_type="application/json")

        except:
            return HttpResponseBadRequest(json.dumps({"detail": "PUT missing body with content_type: application/json"}), content_type="application/json")

        request_body = serializer.validated_data
        follower_url = str(request_body["url"])

        # Validate the follower id matches the id supplied in url
        follower_id = follower_url.split("followers/")[-1].strip()
        
        if follower_id != foreign_author_id.strip():
            return HttpResponseBadRequest(json.dumps({"detail": "author id in URL does not match id in PUT body"}), content_type="application/json")

        data = dict()
        data["author_id"] = author_id
        data["follower_url"] = follower_url
        serializer = FollowerModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps(serializer.data))
        else:
            return HttpResponseBadRequest(json.dumps({"detail": "error when storing to database", "error": serializer.errors}), content_type="application/json")

        

    def delete_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists

    def check_follower(self, request, author_id=None, foreign_author_id=None):
        get_object_or_404(User, pk=author_id) # Check if user exists
