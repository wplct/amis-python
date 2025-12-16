from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from amis_python.models import File
from amis_python.schema import ImageSerializer
from my_app.models import Domain




class DomainSerializer(serializers.ModelSerializer):
    logo = ImageSerializer()
    class Meta:
        model = Domain
        fields = ['id', 'name', 'logo']

    def create(self, validated_data):
        logo_data = validated_data.pop('logo')
        logo = File.objects.get(id=logo_data['id'])
        domain = Domain.objects.create(logo=logo, **validated_data)
        return domain
    def update(self, instance, validated_data):
        logo_data = validated_data.pop('logo')
        logo = File.objects.get(id=logo_data['id'])
        instance.logo = logo
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.order_by('-id').all()
    serializer_class = DomainSerializer


    @action(methods=['POST'], detail=False)
    def test(self, request):
        pass

    @action(methods=['POST'], detail=True)
    def test2(self, request):
        pass