from rest_framework import permissions
from elearning.models import Course


class IsCourseOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        course = request.data.get("course")
        if course:
            is_course_own = Course.objects.filter(
                id=course, instructor=request.user
            ).exists()
            return is_course_own
        return True
