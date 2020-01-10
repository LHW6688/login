from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """用户模型类,继承并修改系统自带模型类"""

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户个人信息'
        verbose_name_plural = verbose_name