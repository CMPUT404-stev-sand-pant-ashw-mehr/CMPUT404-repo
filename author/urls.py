# from .views import ListAuthors
from django.urls.conf import path, re_path
from .api import AuthorViewSet

urlpatterns = [
    re_path(r"^authors/?$", AuthorViewSet.as_view({"get": "list"})),
    re_path(r'^author/(?P<author_id>[a-z0-9-\.-]+)/?$',
            AuthorViewSet.as_view({"get": "get_author", "post": "update"})),
    re_path(r'^author/(?P<author_id>(http://|https://)[a-z0-9\.-:]+(/author/)[a-z0-9\.-]+)/?$',
            AuthorViewSet.as_view({"get": "get_author", "post": "update"}))
]
