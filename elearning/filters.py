import django_filters
from .models import Subject


class CharInFilter(django_filters.CharFilter, django_filters.BaseInFilter):
    pass


class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = ["is_published"]
