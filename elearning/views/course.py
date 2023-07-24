from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from elearning.models import Course
from elearning.serializers.course import (
    CourseReadSerializer,
    CourseWriteSerializer,
)
from elearning.filters import CourseFilter
from elearning.pagination import DefaultPagination


class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseReadSerializer
    write_serializer_class = CourseWriteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CourseFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="mark-as-draft",
    )
    def mark_as_draft(self, request, pk=None):
        course = self.get_object()
        course.mark_as_draft()
        serializer = self.serializer_class(course)
        return Response(serializer.data)
