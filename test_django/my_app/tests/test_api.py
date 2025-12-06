# from django.test import TestCase
# from django.urls import reverse
#
#
# class ApiTestCase(TestCase):
#     def test_api(self):
#         # from my_app.urls import api
#         from ninja import NinjaAPI
#         api = NinjaAPI(urls_namespace="myapp_api")  # ← 关键！
#
#         @api.post("/amis/api/mock2/form/saveForm2")
#         def save_form2(request, data: dict):
#             return {"status": "success"}
#
#         _ = api.urls
#         op = save_form2._ninja_operation
#         print(type(op))
#         print(dir(op))
#         print(op.path)
#         url_name = op.url_name
#         full_path = reverse(url_name)
#         print(full_path)  # 输出: /amis/api/mock2/form/saveForm1
