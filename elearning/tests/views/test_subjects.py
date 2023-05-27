from rest_framework.test import APITestCase
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
from users.factories import UserFactory
from elearning.factories import SubjectFactory


class ViewSubjectsTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_1 = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.subject_1 = SubjectFactory(
            author=self.user, is_published=True, title="subject 1", description="desc 1"
        )
        self.subject_2 =  SubjectFactory(
            author=self.user_1, is_published=True, title="subject 2", description="desc 2"
        )
        self.client.force_authenticate(user=self.user)

    def test_can_only_view_owned_subjects(self):
        response = self.client.get("/subjects/")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.subject_1.id)

    def test_can_only_view_owned_subject(self):
        response = self.client.get(f"/subjects/{self.subject_1.id}/")
        data = response.json()
        self.assertEqual(data["id"], self.subject_1.id)
        self.assertEqual(data["title"], self.subject_1.title)

    def test_cannot_view_not_owned_subject(self):
        subject_by_someone = SubjectFactory()
        response = self.client.get(f"/subjects/{subject_by_someone.id}/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)



class SubjectsFilterTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.subject_1 = SubjectFactory(
            author=self.user, is_published=True, title="subject 1", description="desc 1"
        )
        self.subject_2 = SubjectFactory(
            author=self.user, is_published=True, title="subject 2", description="desc 2"
        )
        self.subject_3 = SubjectFactory(
            author=self.user,
            is_published=False,
            title="subject 3",
            description="desc 3",
        )

    def test_get_published_subjects(self):
        response = self.client.get("/subjects/?is_published=true")
        results = response.json()["results"]

        self.assertEqual(len(results), 2)

    def test_get_draft_subjects(self):
        response = self.client.get("/subjects/?is_published=false")
        results = response.json()["results"]

        self.assertEqual(len(results), 1)

    def test_search_subjects(self):
        response = self.client.get("/subjects/?search=subject")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        response = self.client.get("/subjects/?search=subject 1")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)

        response = self.client.get("/subjects/?search=desc")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        response = self.client.get("/subjects/?search=no results")
        results = response.json()["results"]
        self.assertEqual(len(results), 0)

    def test_get_subjects_by_ordering(self):
        response = self.client.get("/subjects/?ordering=title")
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], self.subject_1.id)

        response = self.client.get("/subjects/?ordering=-title")
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], self.subject_3.id)

class ManageSubjectTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_subject(self):
        payload = {
            "title": "Test subject",
            "description": "test description"
        }
        response = self.client.post('/subjects/', payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])

    def test_author_can_update_its_own_subject(self):
        subject = SubjectFactory(author=self.user)
        payload = {
            "title": "Update Test subject",
            "description": "updated test description"
        }
        response = self.client.patch(f'/subjects/{subject.id}/', payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["title"], payload["title"])
        self.assertEqual(response.json()["description"], payload["description"])

    def test_author_cannot_update_subject_by_other_author(self):
        subject_by_other = SubjectFactory()
        payload = {
            "title": "Update Test subject",
            "description": "updated test description"
        }
        response = self.client.patch(f'/subjects/{subject_by_other.id}/', payload)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)