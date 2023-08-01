from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from elearning.models import Category
from elearning.serializers.category import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
)
from elearning.pagination import DefaultPagination
from elearning.filters import CategoryFilter
from elearning.permissions import IsAdmin


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    write_serializer_class = CategoryWriteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CategoryFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title", "is_active"]
    search_fields = ["title", "description"]

    def get_permissions(self):
        if self.action in ["create", "partial_update"]:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated, IsAdmin],
        url_path="activate",
    )
    def activate(self, request, pk=None):
        category = self.get_object()
        category.activate()
        serializer = self.serializer_class(category)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated, IsAdmin],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None):
        category = self.get_object()
        category.deactivate()
        serializer = self.serializer_class(category)
        return Response(serializer.data)
