from rest_framework import serializers
from users.serializers import UserSerializer
from elearning.serializers.category import CategoryReadSerializer
from elearning.models import Course


class CourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "instructor",
            "category",
        ]

    instructor = UserSerializer()
    category = CategoryReadSerializer()


class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "category"]
