from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class DashboardAPITests(APITestCase):
    def test_only_admin_can_access_stats(self):
        User = get_user_model()
        student = User.objects.create_user(
            email="dashstudent@example.com", password="strongpass123", full_name="Stud", role="STUDENT"
        )
        admin = User.objects.create_user(
            email="dashadmin@example.com", password="strongpass123", full_name="Admin", role="ADMIN"
        )

        self.client.force_authenticate(user=student)
        denied = self.client.get("/api/dashboard/stats/")
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=admin)
        allowed = self.client.get("/api/dashboard/stats/")
        self.assertEqual(allowed.status_code, status.HTTP_200_OK)
        self.assertIn("total_users", allowed.data)
