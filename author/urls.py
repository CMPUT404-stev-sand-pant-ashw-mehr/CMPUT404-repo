# from .views import ListAuthors
from django.urls.conf import path, re_path
from .api import AuthorViewSet

urlpatterns = [
    path("authors/", AuthorViewSet.as_view({"get": "list"})),
    re_path(r'^author/(?P<author_id>\w+)/?$', AuthorViewSet.as_view({"get": "get_author", "post": "update"}))
]