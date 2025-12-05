from django.urls import path
from ninja import NinjaAPI

from . import views

urlpatterns = [
    # API路由配置
    path('api/mock2/page/initData', views.init_data, name='init_data'),
    path('api/mock2/form/saveForm', views.save_form, name='save_form'),
]



from .amis import *
api = NinjaAPI()
from .amis.index.form import router
api.add_router('/form', router)

urlpatterns += [
    path('api/', api.urls),
]