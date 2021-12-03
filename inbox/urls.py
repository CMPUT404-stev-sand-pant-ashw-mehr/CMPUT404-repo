from django.urls.conf import path, re_path
from inbox.api import InboxViewSet

urlpatterns = [
    re_path(r"^author/(?P<author_id>[a-z0-9-\.-]+)/inbox/?$", 
            InboxViewSet.as_view({"get": "get_inbox", "post": "post_inbox", "delete": "delete_inbox"}),
            name="inbox_url"),
    re_path(r"^author/(?P<author_id>[a-z0-9-\.-]+)/inbox/(?P<foreign_id>[a-z0-9-\.-]+)/?$", 
            InboxViewSet.as_view({"delete": "delete_from_inbox"}),
            name="inbox_delete_url")
]