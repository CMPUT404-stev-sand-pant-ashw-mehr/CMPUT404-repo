# from .views import ListAuthors
from rest_framework import routers 
from .api import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')

urlpatterns = router.urls