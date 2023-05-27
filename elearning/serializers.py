from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Subject


class SubjectReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "title",
            "description",
            "is_published",
            "created_at",
            "updated_at",
            "author",
        ]

    author = UserSerializer()

class SubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "title",
            "description",
            "is_published",
        ]