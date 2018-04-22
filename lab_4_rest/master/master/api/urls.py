from django.conf.urls import url, include
from rest_framework import routers
from .views import MatrixViewSet

router = routers.DefaultRouter()
router.register(r'', MatrixViewSet)

urlpatterns = router.urls
