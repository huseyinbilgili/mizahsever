from model_mommy import mommy
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from core.user.models import User


class TestUserViewSet(APITestCase):
    def setUp(self) -> None:
        self.user = mommy.make(User, username="john_doe", is_active=True)
        self.user.set_password("1234")
        self.user.save()

    def test_login(self):
        data = {
            "username": "john_doe",
            "password": "1234"
        }
        response = self.client.post(path=reverse("user:login"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["token"])