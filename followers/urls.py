from django.urls import path
from followers.api import FollowerViewSet

urlpatterns = [
    path('author/<str:author_id>/followers/', FollowerViewSet.as_view({"get":"list"})),
]