import django_filters
from .models import Subject


class CharInFilter(django_filters.CharFilter, django_filters.BaseInFilter):
    pass


class SubjectFilter(django_filters.FilterSet):
    courses = CharInFilter(field_name="courses__id", lookup_expr="in")

    class Meta:
        model = Subject
        fields = ["is_published"]
