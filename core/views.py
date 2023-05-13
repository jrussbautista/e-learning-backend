from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
