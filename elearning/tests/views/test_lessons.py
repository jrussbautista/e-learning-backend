from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from elearning.factories import UserFactory, CourseFactory, LessonFactory
from users.constants import UserRole


class InstructorViewCoursesTests(APITestCase):
    def setUp(self):
        self.instructor = UserFactory(role=UserRole.INSTRUCTOR)
        self.client.force_authenticate(user=self.instructor)

    def test_instructor_can_view_its_owned_lessons(self):
        course = CourseFactory(instructor=self.instructor)
        lesson_1 = LessonFactory(title="title 1", course=course)
        lesson_2 = LessonFactory(title="title 2", course=course)
        response = self.client.get("/lessons/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], lesson_1.id)
        self.assertEqual(results[1]["id"], lesson_2.id)

    def test_instructor_can_view_its_owned_lessons(self):
        course = CourseFactory()  # not owned course by current user
        LessonFactory(title="title 1", course=course)
        LessonFactory(title="title 2", course=course)
        response = self.client.get("/lessons/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 0)


class InstructorManageLessonTests(APITestCase):
    def setUp(self):
        self.instructor = UserFactory()
        self.client.force_authenticate(user=self.instructor)

    def test_create_lesson(self):
        course = CourseFactory(instructor=self.instructor)
        payload = {"title": "Test course", "course": course.id}
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], payload["title"])

    def test_cannot_create_lesson_if_course_payload_is_missing(self):
        payload = {
            "title": "Test course",
        }
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_cannot_create_lesson_if_course_is_not_owned(self):
        course = CourseFactory()  # not owned by current instructor
        payload = {"title": "Test course", "course": course.id}
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
