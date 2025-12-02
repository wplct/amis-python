from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_app'
    
    def ready(self):
        # 导入amis.py文件，确保应用启动时注册默认应用
        from . import amis
