from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course
from reviews.models import Review


class ReviewAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.instructor = User.objects.create_user(
            email="ins3@example.com", password="strongpass123", full_name="Ins", role="INSTRUCTOR"
        )
        self.student = User.objects.create_user(
            email="revstudent@example.com", password="strongpass123", full_name="Stud", role="STUDENT"
        )
        category = Category.objects.create(name="Science", slug="science")
        self.course = Course.objects.create(
            title="Physics",
            description="D",
            price=20,
            level="Intermediate",
            instructor=self.instructor,
            category=category,
            is_published=True,
        )

    def test_student_can_create_review(self):
        self.client.force_authenticate(user=self.student)
        payload = {"student": self.student.id, "course": self.course.id, "rating": 5, "comment": "Great"}
        response = self.client.post("/api/reviews/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
