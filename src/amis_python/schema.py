from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    url = serializers.CharField()
