from rest_framework.routers import DefaultRouter
from .views import DegreeViewSet

router = DefaultRouter()
router.register(r'degrees', DegreeViewSet, basename='degree')

urlpatterns = router.urls