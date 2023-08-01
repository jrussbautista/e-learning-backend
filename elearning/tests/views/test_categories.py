from rest_framework.test import APITestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN
from users.factories import UserFactory
from elearning.factories import CategoryFactory
from users.constants import UserRole


class ViewCategoriesTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.category_1 = CategoryFactory(
            is_active=True, title="category 1", description="desc 1"
        )
        self.category_2 = CategoryFactory(
            is_active=True, title="category 2", description="desc 2"
        )
        self.client.force_authenticate(user=self.user)

    def test_can_view_categories(self):
        response = self.client.get("/categories/")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], self.category_1.id)

    def test_can_view_category(self):
        response = self.client.get(f"/categories/{self.category_1.id}/")
        data = response.json()
        self.assertEqual(data["id"], self.category_1.id)
        self.assertEqual(data["title"], self.category_1.title)


class CategoriesFilterTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.category_1 = CategoryFactory(
            is_active=True, title="category 1", description="desc 1"
        )
        self.category_2 = CategoryFactory(
            is_active=True, title="category 2", description="desc 2"
        )
        self.category_3 = CategoryFactory(
            is_active=False,
            title="category 3",
            description="desc 3",
        )

    def test_get_active_categories(self):
        response = self.client.get("/categories/?is_active=true")
        results = response.json()["results"]

        self.assertEqual(len(results), 2)

    def test_get_not_active_categories(self):
        response = self.client.get("/categories/?is_active=false")
        results = response.json()["results"]

        self.assertEqual(len(results), 1)

    def test_search_categories(self):
        response = self.client.get("/categories/?search=category")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        response = self.client.get("/categories/?search=category 1")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)

        response = self.client.get("/categories/?search=desc")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        response = self.client.get("/categories/?search=no results")
        results = response.json()["results"]
        self.assertEqual(len(results), 0)

    def test_get_categories_by_ordering(self):
        response = self.client.get("/categories/?ordering=title")
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], self.category_1.id)

        response = self.client.get("/categories/?ordering=-title")
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], self.category_3.id)


class AdminManageCategoryTests(APITestCase):
    def setUp(self):
        self.admin = UserFactory(role=UserRole.ADMIN)
        self.client.force_authenticate(user=self.admin)

    def test_create_category(self):
        payload = {"title": "Test category", "description": "test description"}
        response = self.client.post("/categories/", payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])

    def test_non_admin_cannot_create_category(self):
        instructor = UserFactory(role=UserRole.INSTRUCTOR)
        self.client.force_authenticate(user=instructor)
        payload = {"title": "Test category", "description": "test description"}
        response = self.client.post("/categories/", payload)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_can_update_category(self):
        category = CategoryFactory()
        payload = {
            "title": "Update Test category",
            "description": "updated test description",
        }
        response = self.client.patch(f"/categories/{category.id}/", payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])

    def test_non_admin_cannot_update_category(self):
        instructor = UserFactory(role=UserRole.INSTRUCTOR)
        self.client.force_authenticate(user=instructor)
        category = CategoryFactory()
        payload = {
            "title": "Update Test category",
            "description": "updated test description",
        }
        response = self.client.patch(f"/categories/{category.id}/", payload)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
