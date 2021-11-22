from django.urls.conf import path, re_path
from inbox.api import InboxViewSet

urlpatterns = [
    re_path(r"^author/(?P<author_id>[a-z0-9-\.-]+)/inbox/?$", 
            InboxViewSet.as_view({"get": "get_inbox", "post": "post_inbox", "delete": "delete_inbox"}),
            name="inbox_url")
]