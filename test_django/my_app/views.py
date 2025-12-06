from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# @csrf_exempt
# def init_data(request):
#     """处理initData API请求，返回包含date字段的JSON响应"""
#     return JsonResponse({
#         "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     })

# @csrf_exempt
# def save_form(request):
#     """处理表单提交请求，返回成功响应"""
#     if request.method == 'POST':
#         # 处理表单数据
#         data = {
#             "status": 0,
#             "msg": "表单提交成功",
#             "data": {
#                 "success": True
#             }
#         }
#         return JsonResponse(data)
#     else:
#         return JsonResponse({"status": 1, "msg": "只支持POST请求"}, status=405)

