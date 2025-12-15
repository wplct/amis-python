import uuid

from django.core.files.base import ContentFile
from django.test import TestCase
from ninja import ModelSchema
from pydantic import BaseModel, ConfigDict

from amis_python.models import File, FileSchema
from my_app.models import Domain


class DomainTestCase(TestCase):


    def test_schema(self):

        class DomainSchema(ModelSchema):
            logo: FileSchema

            class Meta:
                model = Domain
                fields = ["id",'name','description','created_at']

        for field_name, field in DomainSchema.model_fields.items():
            print(field_name, field)

        uploaded = ContentFile(b'test', name='test.txt',)
        logo = File(
            key=str(uuid.uuid4()),
            name=uploaded.name,
            size=uploaded.size,
            type='application/octet-stream',
        )
        logo.file.save(uploaded.name, uploaded)
        logo.save()

        domain = Domain(
            name='test',
            logo=logo,
        )
        domain.save()



        # d = DomainSchema.from_orm(domain)

