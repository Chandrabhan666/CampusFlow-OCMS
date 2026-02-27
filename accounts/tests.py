from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAPITests(APITestCase):
    def test_register_and_me_flow(self):
        payload = {
            "email": "student1@example.com",
            "password": "strongpass123",
            "full_name": "Student One",
            "role": "STUDENT",
        }
        response = self.client.post("/api/accounts/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        User = get_user_model()
        user = User.objects.get(email=payload["email"])
        self.client.force_authenticate(user=user)
        me = self.client.get("/api/accounts/me/")
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(me.data["email"], payload["email"])
