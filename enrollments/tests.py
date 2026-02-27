from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course
from enrollments.models import Enrollment


class EnrollmentAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.instructor = User.objects.create_user(
            email="ins2@example.com", password="strongpass123", full_name="Ins", role="INSTRUCTOR"
        )
        self.student1 = User.objects.create_user(
            email="s1@example.com", password="strongpass123", full_name="S1", role="STUDENT"
        )
        self.student2 = User.objects.create_user(
            email="s2@example.com", password="strongpass123", full_name="S2", role="STUDENT"
        )
        category = Category.objects.create(name="Math", slug="math")
        self.course = Course.objects.create(
            title="Algebra",
            description="C",
            price=0,
            level="Beginner",
            instructor=self.instructor,
            category=category,
            is_published=True,
        )
        Enrollment.objects.create(student=self.student1, course=self.course)
        Enrollment.objects.create(student=self.student2, course=self.course)

    def test_student_sees_only_own_enrollments(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get("/api/enrollments/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
