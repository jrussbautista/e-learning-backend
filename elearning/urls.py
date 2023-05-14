from rest_framework_nested import routers
from .views import SubjectViewSet


router = routers.DefaultRouter()
router.register("subjects", SubjectViewSet, basename="subjects")

urlpatterns = router.urls
