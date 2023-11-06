from advertisements.views import AdvertisementViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)

urlpatterns = router.urls