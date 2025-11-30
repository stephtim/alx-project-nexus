from django.test import TestCase
from rest_framework.test import APIClient
from store.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u@example.com", password="pass1234")
        self.client = APIClient()

    def test_token_obtain(self):
        resp = self.client.post("/api/auth/token/", {"email":"u@example.com","password":"pass1234"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)
