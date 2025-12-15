# from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse

from amis_python import Api
from amis_python.build_amis.form import ViewSetForm
from amis_python.builder.crud2 import CRUD2, CRUD2Mode


class ViewSetCRUD:
    def __init__(self, view_set: GenericAPIView, basename=None):
        self.view_set = view_set
        self.serializer = view_set.get_serializer_class()()
        self.view_form = ViewSetForm(view_set, basename)
        if not basename:
            self.basename = view_set.queryset.model._meta.model_name
        else:
            self.basename = basename
    def get_api(self):
        return Api(
            method="get",
            url=reverse(f"{self.basename}-list"),
        )

    def to_crud(self, **kwargs):
        return CRUD2(
            mode=CRUD2Mode.TABLE2,
            api=self.get_api(),
            columns=self.view_form.get_list_items(static=True),
            **kwargs
        )



