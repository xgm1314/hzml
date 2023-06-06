from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表 """
    name = models.CharField(verbose_name='名称', max_length=20, unique=True, help_text='部门名称')
    Superior = models.ForeignKey(verbose_name='上级部门', to='self', on_delete=models.SET_NULL, related_name='subs',
                                 null=True, blank=True, help_text='上级部门')

    class Meta:
        db_table = 'tb_departments'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
