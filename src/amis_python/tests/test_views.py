from unittest import TestCase
from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from amis_python.views import (
    GetAmisAppConfig,
    GetPageConfig,
    GetLoginConfig,
    LoginView,
    LogoutView,
    CurrentUserView,
    UploadView,
    UploadImageView
)
from amis_python.models import File


class ApiTestCase(TestCase):
    """API测试基类"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = APIClient()
        self.factory = RequestFactory()
        
        # 创建测试用户
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
    
    def tearDown(self):
        """清理测试环境"""
        self.user.delete()


class AuthenticationApiTestCase(ApiTestCase):
    """认证相关API测试"""
    
    def test_login_success(self):
        """测试登录成功"""
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post("/amis/api/login", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data["data"])
        self.assertEqual(response.data["data"]["username"], self.username)
    
    def test_login_failure(self):
        """测试登录失败"""
        data = {
            "username": self.username,
            "password": "wrongpassword"
        }
        response = self.client.post("/amis/api/login", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], 400)
    
    def test_logout(self):
        """测试登出"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 然后登出
        response = self.client.post("/amis/api/logout")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["status"], 0)
    
    def test_current_user(self):
        """测试获取当前用户信息"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 然后获取当前用户信息
        response = self.client.get("/amis/api/current-user")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["status"], 0)
        self.assertEqual(response.data["data"]["data"]["username"], self.username)
    
    def test_current_user_unauthorized(self):
        """测试未登录时获取当前用户信息"""
        response = self.client.get("/amis/api/current-user")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ConfigApiTestCase(ApiTestCase):
    """配置相关API测试"""
    
    def test_get_login_config(self):
        """测试获取登录配置"""
        response = self.client.get("/amis/api/login/config")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data["data"])
    
    def test_get_amis_app_config_unauthorized(self):
        """测试未登录时获取应用配置"""
        response = self.client.get("/amis/api/config")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_amis_app_config_authorized(self):
        """测试登录后获取应用配置"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 然后获取应用配置
        response = self.client.get("/amis/api/config")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_page_config_unauthorized(self):
        """测试未登录时获取页面配置"""
        response = self.client.get("/amis/api/page/config")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_page_config_authorized(self):
        """测试登录后获取页面配置"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 然后获取页面配置
        response = self.client.get("/amis/api/page/config")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UploadApiTestCase(ApiTestCase):
    """文件上传API测试"""
    
    def test_upload_file_unauthorized(self):
        """测试未登录时上传文件"""
        # 创建一个测试文件
        test_file = "test.txt"
        test_content = "test content"
        
        response = self.client.post("/amis/api/upload", {
            "file": (test_file, test_content, "text/plain")
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_upload_file_authorized(self):
        """测试登录后上传文件"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 创建一个测试文件
        test_file = "test.txt"
        test_content = "test content"
        
        response = self.client.post("/amis/api/upload", {
            "file": (test_file, test_content, "text/plain")
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["status"], 0)
    
    def test_upload_image_unauthorized(self):
        """测试未登录时上传图片"""
        # 创建一个测试图片
        test_file = "test.png"
        test_content = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        response = self.client.post("/amis/api/upload/image", {
            "file": (test_file, test_content, "image/png")
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_upload_image_authorized(self):
        """测试登录后上传图片"""
        # 先登录
        self.client.login(username=self.username, password=self.password)
        
        # 创建一个测试图片
        test_file = "test.png"
        test_content = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        response = self.client.post("/amis/api/upload/image", {
            "file": (test_file, test_content, "image/png")
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["status"], 0)
