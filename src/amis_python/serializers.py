from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    登录请求序列化器
    """

    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, max_length=128, write_only=True)

    def validate(self, attrs):
        """
        验证用户名和密码
        """
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("用户名或密码错误")
        else:
            raise serializers.ValidationError("必须提供用户名和密码")

        attrs["user"] = user
        return attrs
