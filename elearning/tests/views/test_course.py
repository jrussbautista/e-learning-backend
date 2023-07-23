from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from elearning.factories import UserFactory, CategoryFactory, CourseFactory
from elearning.constants import CourseStatus


class ViewCoursesTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_instructor_can_view_its_owned_courses(self):
        course_1 = CourseFactory(
            title="title 1", description="desc 1", instructor=self.user
        )
        course_2 = CourseFactory(
            title="title 2", description="desc 2", instructor=self.user
        )
        response = self.client.get("/courses/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], course_1.id)
        self.assertEqual(results[1]["id"], course_2.id)

    def test_instructor_cannot_view_not_owned_courses(self):
        owned_course = CourseFactory(instructor=self.user)
        not_owned_course = CourseFactory()
        response = self.client.get("/courses/")
        results = response.json()["results"]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], owned_course.id)

    def test_instructor_can_view_its_owned_course(self):
        owned_course = CourseFactory(instructor=self.user)
        response = self.client.get(f"/courses/{owned_course.id}/")
        data = response.json()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(data["id"], owned_course.id)
        self.assertEqual(data["title"], owned_course.title)

    def test_instructor_cannot_view_not_owned_course(self):
        not_owned_course = CourseFactory()
        response = self.client.get(f"/courses/{not_owned_course.id}/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class ManageCourseTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        category = CategoryFactory()
        payload = {
            "title": "Test course",
            "description": "test course",
            "category": category.id,
        }
        response = self.client.post("/courses/", payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])
        self.assertEqual(response.json()["category"]["id"], payload["category"])

    def test_create_course_should_be_for_review_by_default(self):
        category = CategoryFactory()
        payload = {
            "title": "Test course",
            "description": "test course",
            "category": category.id,
        }
        response = self.client.post("/courses/", payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["status"], CourseStatus.FOR_REVIEW)

    def test_cannot_create_course_if_category_payload_is_missing(self):
        payload = {
            "title": "Test course",
            "description": "test course",
        }
        response = self.client.post("/courses/", payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_instructor_can_update_owned_courses(self):
        course = CourseFactory(instructor=self.user)
        payload = {
            "title": "Updated course title",
            "description": "Update course description",
        }
        response = self.client.patch(f"/courses/{course.id}/", payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])

    def test_instructor_cannot_update_not_owned_courses(self):
        course = CourseFactory()
        payload = {
            "title": "Updated course title",
            "description": "Update course description",
        }
        response = self.client.patch(f"/courses/{course.id}/", payload)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
