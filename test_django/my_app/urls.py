from django.urls import path
from . import views

urlpatterns = [
    # API路由配置
    path('api/mock2/page/initData', views.init_data, name='init_data'),
    path('api/mock2/form/saveForm', views.save_form, name='save_form'),
]
