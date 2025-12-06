from django.db import models

# Create your models here.


class Domain(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '主体'
        verbose_name_plural = '主体管理'

