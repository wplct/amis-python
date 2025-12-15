import os
import uuid

from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse

from amis_python.builder.form.build import SchemaFormBuild
from my_app.api.domain_api import DomainSerializer, DomainViewSet
from my_app.models import Domain

class DomainTestCase(TestCase):


    def test_schema(self):

        # print(DomainSerializer)
        #
        # print(dir(DomainSerializer))
        #
        # print(DomainSerializer().get_fields())

        SerializerToForm(DomainSerializer()).to_form()

    def test_get_url(self):
        print(reverse('domain-list'))
        print(DomainViewSet.queryset.model._meta.model_name)

        # d = DomainSchema.from_orm(domain)

