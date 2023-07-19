from rest_framework.test import APITestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from elearning.factories import UserFactory, CategoryFactory


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

    def test_cannot_create_course_if_category_payload_is_missing(self):
        payload = {
            "title": "Test course",
            "description": "test course",
        }
        response = self.client.post("/courses/", payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
