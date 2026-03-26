from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password)


class AuthenticationApiTestCase(ApiTestCase):
    def test_login_success(self):
        response = self.client.post(
            "/amis/api/login",
            data={"username": self.username, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertEqual(response.data["data"]["username"], self.username)

    def test_login_failure(self):
        response = self.client.post(
            "/amis/api/login",
            data={"username": self.username, "password": "wrongpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 400)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post("/amis/api/logout")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertEqual(response.data["data"]["status"], 0)

    def test_current_user(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get("/amis/api/current_user")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertEqual(response.data["data"]["data"]["username"], self.username)

    def test_current_user_unauthorized(self):
        response = self.client.get("/amis/api/current_user")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ConfigApiTestCase(ApiTestCase):
    def test_get_login_config(self):
        response = self.client.get("/amis/login/config/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertIn("title", response.data["data"])

    def test_get_amis_app_config_unauthorized(self):
        response = self.client.get("/amis/config/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UploadApiTestCase(ApiTestCase):
    def test_upload_file_unauthorized(self):
        test_file = SimpleUploadedFile("test.txt", b"test content", content_type="text/plain")
        response = self.client.post("/amis/upload", {"file": test_file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_authorized(self):
        self.client.login(username=self.username, password=self.password)
        test_file = SimpleUploadedFile("test.txt", b"test content", content_type="text/plain")

        response = self.client.post("/amis/upload", {"file": test_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertEqual(response.data["msg"], "上传成功")
        self.assertEqual(response.data["data"]["name"], "test.txt")
        self.assertTrue(response.data["data"]["value"].startswith("files/"))
        self.assertIn("url", response.data["data"])

    def test_upload_image_unauthorized(self):
        test_file = SimpleUploadedFile("test.png", b"fake-image", content_type="image/png")
        response = self.client.post("/amis/upload_img", {"file": test_file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_image_authorized(self):
        self.client.login(username=self.username, password=self.password)
        test_file = SimpleUploadedFile("test.png", b"fake-image", content_type="image/png")

        response = self.client.post("/amis/upload_img", {"file": test_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 0)
        self.assertEqual(response.data["msg"], "上传成功")
        self.assertEqual(response.data["data"]["name"], "test.png")
        self.assertTrue(response.data["data"]["id"].startswith("files/"))
        self.assertEqual(response.data["data"]["value"], response.data["data"]["url"])
        self.assertIn("url", response.data["data"])
