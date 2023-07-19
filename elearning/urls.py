from rest_framework_nested import routers
from elearning.views.category import CategoryViewSet
from elearning.views.course import CourseViewSet


router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("courses", CourseViewSet, basename="courses")

urlpatterns = router.urls
