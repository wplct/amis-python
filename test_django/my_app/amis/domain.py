import time

from amis_python import register_page, Page
from amis_python.build_amis.crud import ViewSetCRUD
from amis_python.build_amis.form import ViewSetForm
from my_app.api.domain_api import DomainSerializer, DomainViewSet

def get_page(request):
    return Page(
        # init_api='/test_data?data={"id":50}',
        title="主体测试",
        body=[
            # {"type": "link", "body": "${"+str(time.time())+"|date}"},
            {"type": "link", "body": "${"+str(time.time()-10000)+'|date}'},
            # ViewSetForm(DomainViewSet()).to_create_form(),
            ViewSetCRUD(DomainViewSet(),request).to_crud(),
        ]
    )
register_page("主体测试", "/domain", get_page)
