from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer
from .pagination import DefaultPagination
from .filters import SubjectFilter


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = SubjectFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title", "is_published"]
    search_fields = ["title", "description"]
