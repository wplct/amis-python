from amis_python import register_page, Page
from amis_python.build_amis.form import ViewSetForm
from my_app.api.domain_api import DomainSerializer, DomainViewSet

def get_page():
    return Page(
        # init_api='/test_data?data={"id":50}',
        title="上传测试",
        data={"id":50},
        body=[
            # ViewSetForm(DomainViewSet()).to_create_form(),
            ViewSetForm(DomainViewSet()).to_detail_form(debug=True,wrap_with_panel=True),
        ]
    )
register_page("上传测试", "/upload", get_page)
