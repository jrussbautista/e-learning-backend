from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description", "is_active", "created_at", "updated_at"]

    author = UserSerializer()


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "description",
            "is_active",
        ]
