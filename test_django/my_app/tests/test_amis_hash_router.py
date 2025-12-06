from django.test import TestCase

class AmisHashRouterTest(TestCase):
    """测试 AMIS 应用的 hash 路由功能"""
    
    def test_amis_index(self):
        """测试 AMIS 应用的首页是否可以正常访问"""
        response = self.client.get('/amis/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AMIS Python Demo')
        # self.assertContains(response, 'routerMode: \'hash\'')
        
    def test_amis_config(self):
        """测试 AMIS 应用的配置是否可以正常获取"""
        response = self.client.get('/amis/config/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('brandName', response.json())
        self.assertEqual(response.json()['brandName'], '测试应用')
        
    def test_amis_page_config(self):
        """测试 AMIS 应用的页面配置是否可以正常获取"""
        response = self.client.get('/amis/page/test/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.json())
        self.assertEqual(response.json()['title'], '测试页面')