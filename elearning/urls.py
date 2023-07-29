from rest_framework_nested import routers
from elearning.views.category import CategoryViewSet
from elearning.views.course import CourseViewSet
from elearning.views.lesson import LessonViewSet


router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("courses", CourseViewSet, basename="courses")
router.register("lessons", LessonViewSet, basename="lessons")

urlpatterns = router.urls
