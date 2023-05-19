from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.department.models import Department
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    """ 员工表 """
    # identifier=models.CharField(max_length=40,unique=True)
    # USERNAME_FIELD='identifier'
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    # superuser_choices = (
    #     (0, '非管理员'),
    #     (1, '管理员')
    # )
    # username = models.CharField(verbose_name='姓名', max_length=6)
    # email = models.EmailField(verbose_name='邮箱')
    # password = models.CharField(verbose_name='密码', max_length=32)
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)
    # is_superuser = models.SmallIntegerField(verbose_name='是否是管理员', choices=superuser_choices, default=0)
    date_joined = models.DateTimeField(verbose_name='入职日期')
    one_department = models.ForeignKey(verbose_name='一级部门', to=Department, on_delete=models.PROTECT, default='')
    # two_department = models.ForeignKey(verbose_name='二级部门', to=Department, on_delete=models.PROTECT, default='')
    # three_department = models.ForeignKey(verbose_name='三级部门', to=Department, on_delete=models.PROTECT, default='')
    # four_department = models.ForeignKey(verbose_name='四级部门', to=Department, on_delete=models.PROTECT, default='')
    position = models.CharField(verbose_name='职位', max_length=10)
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True)
    birthday = models.DateTimeField(verbose_name='出生日期')
    image = models.ImageField(verbose_name='头像', null=True, blank=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
