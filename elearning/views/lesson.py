from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from elearning.models import Lesson
from elearning.serializers.lesson import (
    LessonReadSerializer,
    LessonWriteSerializer,
)
from elearning.filters import LessonFilter
from elearning.pagination import DefaultPagination
from elearning.permissions import IsCourseOwner
from users.constants import UserRole


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LessonReadSerializer
    write_serializer_class = LessonWriteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = LessonFilter
    pagination_class = DefaultPagination
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return [IsAuthenticated(), IsCourseOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == UserRole.INSTRUCTOR:
            return Lesson.objects.filter(course__instructor=self.request.user)
        return Lesson.objects.all() 
