import datetime
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from pydantic import ConfigDict
from amis_python.builder import BaseModel


def uuid_filename(instance, filename):
    """upload_to 回调：直接返回 files/YYYY/MM/DD/<uuid>.<ext>"""
    ext = os.path.splitext(filename)[1] or '.ext'
    new_name = f'{instance.key}{ext}'
    now = datetime.datetime.now()
    return f'files/{now:%Y/%m/%d}/{new_name}'


class File(models.Model):
    # 新增：文件内容 hash（唯一）
    key = models.CharField(max_length=64, unique=True, db_index=True)
    file = models.FileField(upload_to=uuid_filename)
    name = models.CharField(max_length=255)          # 原始文件名
    size = models.IntegerField()
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 可选：关联上传者
    # uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def url(self):
        return self.file.url


    class Meta:
        db_table = 'files'
        verbose_name = 'File'
        verbose_name_plural = 'Files'

