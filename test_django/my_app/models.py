from django.db import models

# Create your models here.


class Domain(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name = '主体'
        verbose_name_plural = '主体管理'

