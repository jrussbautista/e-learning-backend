from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from elearning.factories import UserFactory, CourseFactory, LessonFactory
from users.constants import UserRole


class AdminViewLessonsTests(APITestCase):
    def setUp(self):
        self.admin = UserFactory(role=UserRole.ADMIN)
        self.lesson_1 = LessonFactory()
        self.lesson_2 = LessonFactory()
        self.client.force_authenticate(user=self.admin)

    def test_admin_can_view_all_lessons(self):
        response = self.client.get("/lessons/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 2)


class InstructorViewLessonsTests(APITestCase):
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

    def test_instructor_cannot_view_its_owned_lessons(self):
        course = CourseFactory()  # not owned course by current user
        LessonFactory(title="title 1", course=course)
        LessonFactory(title="title 2", course=course)
        response = self.client.get("/lessons/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 0)

    def test_instructor_can_view_its_owned_lesson(self):
        owned_course = CourseFactory(instructor=self.instructor)
        lesson = LessonFactory(course=owned_course)
        response = self.client.get(f"/lessons/{lesson.id}/")
        data = response.json()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["id"], lesson.id)
        self.assertEqual(data["title"], lesson.title)

    def test_instructor_cannot_view_not_owned_lesson(self):
        lesson = LessonFactory()
        response = self.client.get(f"/lessons/{lesson.id}/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class InstructorManageLessonTests(APITestCase):
    def setUp(self):
        self.instructor = UserFactory(role=UserRole.INSTRUCTOR)
        self.client.force_authenticate(user=self.instructor)

    def test_create_lesson(self):
        course = CourseFactory(instructor=self.instructor)
        payload = {"title": "Test lesson", "course": course.id}
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], payload["title"])

    def test_cannot_create_lesson_if_course_payload_is_missing(self):
        payload = {
            "title": "Test lesson",
        }
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_cannot_create_lesson_if_course_is_not_owned(self):
        course = CourseFactory()  # not owned by current instructor
        payload = {"title": "Test lesson", "course": course.id}
        response = self.client.post("/lessons/", payload)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_update_lesson(self):
        lesson = LessonFactory(course__instructor=self.instructor)
        course = CourseFactory(instructor=self.instructor)
        payload = {"title": "Updated test lesson", "course": course.id}
        response = self.client.patch(f"/lessons/{lesson.id}/", payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["title"], payload["title"])

    def test_cannot_update_lesson_with_not_owned_course(self):
        lesson = LessonFactory()
        course = CourseFactory()
        payload = {"title": "Updated test lesson", "course": course.id}
        response = self.client.patch(f"/lessons/{lesson.id}/", payload)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_delete_lesson(self):
        course = CourseFactory(instructor=self.instructor)
        lesson = LessonFactory(course=course)
        response = self.client.delete(f"/lessons/{lesson.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_cannot_delete_not_owned_lesson(self):
        lesson = LessonFactory()
        response = self.client.delete(f"/lessons/{lesson.id}/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_can_activate_lesson(self):
        lesson = LessonFactory(course__instructor=self.instructor)
        response = self.client.post(f"/lessons/{lesson.id}/activate/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        json = response.json()
        self.assertTrue(json["is_active"])

    def test_cannot_activate_not_owned_lesson(self):
        lesson = LessonFactory()
        response = self.client.post(f"/lessons/{lesson.id}/activate/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_can_deactivate_lesson(self):
        lesson = LessonFactory(course__instructor=self.instructor)
        response = self.client.post(f"/lessons/{lesson.id}/deactivate/")
        json = response.json()
        self.assertFalse(json["is_active"])

    def test_cannot_deactivate_not_owned_lesson(self):
        lesson = LessonFactory()
        response = self.client.post(f"/lessons/{lesson.id}/deactivate/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
