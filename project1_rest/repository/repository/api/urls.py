from django.conf.urls import url, include
from rest_framework import routers
from .views import PairViewSet

router = routers.DefaultRouter()
router.register(r'', PairViewSet)

urlpatterns = router.urls
