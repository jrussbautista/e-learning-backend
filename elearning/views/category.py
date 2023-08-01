from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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
        return [IsAuthenticated()]
