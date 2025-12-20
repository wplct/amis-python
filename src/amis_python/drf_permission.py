from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """
    只允许安全请求（HEAD/GET/OPTIONS），
    拒绝所有会修改数据的动作（POST/PUT/PATCH/DELETE）。
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS