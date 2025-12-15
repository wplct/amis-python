from rest_framework import serializers

from amis_python.models import File


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    class Meta:
        model = File
        fields = ['id', 'name', 'url']