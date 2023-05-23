from rest_framework.test import APITestCase
from users.factories import UserFactory
from elearning.factories import SubjectFactory


class ViewSubjectTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.subject = SubjectFactory(
            author=self.user, is_published=True, title="subject 1", description="desc 1"
        )
        self.client.force_authenticate(user=self.user)

    def get_subject_details_by_id(self):
        response = self.client.get(f"/subjects/{self.subject.id}/")
        details = response.json()
        self.assertEqual(details.id, self.subject.id)
        self.assertEqual(details.title, self.subject.title)


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