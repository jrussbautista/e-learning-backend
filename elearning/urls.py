from rest_framework_nested import routers
from elearning.views.category import CategoryViewSet


router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = router.urls
