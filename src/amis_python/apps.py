from django.apps import AppConfig


class AmisPythonConfig(AppConfig):
    """
    amis-python Django 应用配置
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amis_python'
    verbose_name = 'Amis Python'
    
    def ready(self):
        """
        应用就绪时执行的初始化代码
        """
        # 可以在这里添加一些初始化逻辑
        pass