from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
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
