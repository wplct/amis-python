from django.urls import path
from amis_python.ninja_api import AmisAPI, amis_api
from . import views

urlpatterns = [
    # API路由配置
    # path('api/mock2/page/initData', views.init_data, name='init_data'),
    # path('api/mock2/form/saveForm', views.save_form, name='save_form'),
]
@amis_api.get('/test/test')
def index(request):
    return {"date": "2023-01-01"}
