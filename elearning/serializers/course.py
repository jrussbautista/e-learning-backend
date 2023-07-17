from rest_framework import serializers
from users.serializers import UserSerializer
from elearning.models import Course


class CourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "status", "created_at", "instructor"]

    instructor = UserSerializer()


class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "category"]
