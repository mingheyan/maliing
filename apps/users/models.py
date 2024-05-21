from django.db import models
from  django.contrib.auth.models import AbstractUser


# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=11, unique=True)
#
#     def __str__(self):
#         return self.name
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = 'verbose_name'
    def __str__(self):
        return self.username