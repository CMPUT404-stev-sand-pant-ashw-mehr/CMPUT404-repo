# from .views import ListAuthors
from django.urls.conf import path
from .api import AuthorViewSet

urlpatterns = [
    path("authors/", AuthorViewSet.as_view({"get": "list"})),
    path("author/<str:pk>", AuthorViewSet.as_view({"get": "retrieve", "post": "create"}))
]