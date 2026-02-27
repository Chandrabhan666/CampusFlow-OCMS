from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course


class CourseAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.instructor = User.objects.create_user(
            email="ins@example.com", password="strongpass123", full_name="Ins", role="INSTRUCTOR"
        )
        self.category = Category.objects.create(name="Programming", slug="programming")
        Course.objects.create(
            title="Public Course",
            description="A",
            price=0,
            level="Beginner",
            instructor=self.instructor,
            category=self.category,
            is_published=True,
        )
        Course.objects.create(
            title="Draft Course",
            description="B",
            price=10,
            level="Advanced",
            instructor=self.instructor,
            category=self.category,
            is_published=False,
        )

    def test_public_list_shows_only_published_courses(self):
        response = self.client.get("/api/courses/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Public Course", titles)
        self.assertNotIn("Draft Course", titles)
