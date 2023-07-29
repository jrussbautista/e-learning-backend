from rest_framework import serializers
from elearning.serializers.course import CourseReadSerializer
from elearning.models import Lesson


class LessonReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "is_active",
            "course",
            "created_at",
        ]

    course = CourseReadSerializer()


class LessonWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["title", "course"]
