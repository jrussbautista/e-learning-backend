from django.db import models
from django.conf import settings
from .constants import CourseStatus


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        choices=CourseStatus.choices,
        default=CourseStatus.FOR_REVIEW,
        max_length=100,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="courses"
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )

    def mark_as_draft(self):
        self.status = CourseStatus.DRAFT
        self.save()


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()


class Chapter(models.Model):
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="chapters"
    )
