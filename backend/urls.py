from django.urls import include, path
from .views import ListPosts
from rest_framework import routers 
from .api import InboxViewSet, PostViewSet

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = routers.DefaultRouter()
router.register('posts', PostViewSet, 'posts')
router.register('inbox', InboxViewSet, 'inbox')

urlpatterns = router.urls

# urlpatterns = [
#     path('posts', ListPosts.as_view()),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]