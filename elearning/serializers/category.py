from rest_framework import serializers
from elearning.models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description", "is_active", "created_at", "updated_at"]


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "description",
            "is_active",
        ]
