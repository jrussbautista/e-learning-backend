from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from elearning.models import Course
from elearning.serializers.course import (
    CourseReadSerializer,
    CourseWriteSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseReadSerializer
    write_serializer_class = CourseWriteSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
