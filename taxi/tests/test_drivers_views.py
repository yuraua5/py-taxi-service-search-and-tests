from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVERS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="123456test",
            license_number="TEST12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="test1",
            password="123456test2",
            license_number="TET12345"
        )
        response = self.client.get(DRIVERS_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "passtest123",
            "password2": "passtest123",
            "first_name": "Ivan",
            "last_name": "Testovuy",
            "license_number": "TES11234"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_search_driver_list(self):
        response = self.client.get(DRIVERS_LIST_URL, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="test"))
        )
