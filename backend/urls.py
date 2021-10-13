from django.urls import include, path
from .views import ListPosts

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('posts', ListPosts.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]