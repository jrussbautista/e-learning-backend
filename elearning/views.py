from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectReadSerializer, SubjectWriteSerializer
from .pagination import DefaultPagination
from .filters import SubjectFilter



class SubjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectReadSerializer
    write_serializer_class = SubjectWriteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = SubjectFilter
    pagination_class = DefaultPagination
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title", "is_published"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        queryset = Subject.objects.filter(author=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)