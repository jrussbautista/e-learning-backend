import django_filters
from .models import Category


class CharInFilter(django_filters.CharFilter, django_filters.BaseInFilter):
    pass


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ["is_active"]

