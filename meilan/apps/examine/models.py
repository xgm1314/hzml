from django.db import models

from apps.department.models import Department
from apps.user.models import User

"""
两个时间只差计算测试
from datetime import *
str_time='2023-06-05 13:05:00'
origin_time=datetime.strptime(str_time,'%Y-%m-%d %H:%M:%S')
now_time=datetime.now()
total_time=now_time-origin_time
print(total_time)

定义函数,计算两个时间的差值
from datetime import *
import time
def dateTime(str_time, end_time):
    origin_time = datetime.strptime(str_time, '%Y-%m-%d')
    if end_time == '':
        end_time = time.strftime('%Y-%m-%d', time.localtime())
    now_time = datetime.strptime(end_time, '%Y-%m-%d')
    # print(now_time)
    total_time = now_time - origin_time
    # print('相距:%s' % total_time)
    return total_time
if __name__ == '__main__':
    str_time = input('输入开始时间:')
    end_time = input('输入结束时间:')
    total_time = dateTime(str_time, end_time)
    print('相距%s'%total_time)
 
 
输出 天 时 分 秒  
import math
import time
from datetime import *


def formatTime2Custom(day, Time):
    hour = 60 * 60
    min = 60
    if Time < 60:
        return "%d天0小时0分钟%d秒" % (day, math.ceil(Time))
    elif Time >= hour:
        hours = divmod(Time, hour)
        # print(hours)
        if hours[1] > min:
            mins = divmod(hours[1], min)
            return "%d天%d小时%s分%s秒" % (day, hours[0], mins[0], mins[1])
        return "%d天%d小时0分%s秒" % (day, hours[0], hours[1])
    elif Time >= min:
        mins = divmod(Time, min)
        # print(mins)
        return "%d天0小时%d分钟%s秒" % (day, mins[0], mins[1])


if __name__ == '__main__':
    from datetime import *

    start_time = input('请输入开始时间:(格式为0000-00-00 00:00:00)')
    end_time = input('请输入结束时间:(格式为0000-00-00 00:00:00)')
    origin_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if end_time == '':
        end_time = datetime.now()
    else:
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    total_time_s = (end_time - origin_time).seconds
    total_time_day = (end_time - origin_time).days
    res = formatTime2Custom(total_time_day, total_time_s)
    print(res)
"""


# Create your models here.
class Examine(models.Model):
    """ 审批表 """
    department = models.ForeignKey(verbose_name='部门', to=Department, on_delete=models.CASCADE, related_name='+',
                                   help_text='部门')
    one_examine = models.ForeignKey(verbose_name='一级审批', to=User, on_delete=models.CASCADE,
                                    related_name='+',
                                    help_text='一级审批')
    two_examine = models.ForeignKey(verbose_name='二级审批', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='+', help_text='二级审批')
    three_examine = models.ForeignKey(verbose_name='三级审批', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='+', help_text='三级审批')
    four_examine = models.ForeignKey(verbose_name='四级审批', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='+', help_text='四级审批')
    five_examine = models.ForeignKey(verbose_name='五级审批', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='+', help_text='五级审批')
    one_copy = models.ForeignKey(verbose_name='抄送人1', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='+', help_text='抄送人1')
    two_copy = models.ForeignKey(verbose_name='抄送人2', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='+', help_text='抄送人2')
    three_copy = models.ForeignKey(verbose_name='抄送人3', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='+', help_text='抄送人3')
    four_copy = models.ForeignKey(verbose_name='抄送人4', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='+', help_text='抄送人4')
    five_copy = models.ForeignKey(verbose_name='抄送人5', to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='+', help_text='抄送人5')

    class Meta:
        db_table = 'tb_examine'
        verbose_name = '审批表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.department


class OverTime(models.Model):
    """ 加班表 """
    examine_id = models.BigIntegerField(verbose_name='审批编号', primary_key=True, unique=True, help_text='审批编号')
    name = models.ForeignKey(verbose_name='提交人', to=User, related_name='name', on_delete=models.CASCADE,
                             help_text='提交人', null=True, blank=True)
    data = models.DateTimeField(verbose_name='提交时间', help_text='提交时间')
    department = models.ForeignKey(verbose_name='部门', to=Department, on_delete=models.CASCADE, help_text='部门')
    reason = models.CharField(verbose_name='事由', max_length=32, help_text='事由')
    start_data = models.DateTimeField(verbose_name='开始时间', help_text='开始时间')
    end_data = models.DateTimeField(verbose_name='结束时间', help_text='结束时间')
    duration = models.CharField(verbose_name='时长', max_length=16, help_text='时长')
    examines = models.ForeignKey(verbose_name='审批数据', to=Examine, on_delete=models.CASCADE, default='',
                                 help_text='审批流程')
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)
    _data = models.DateTimeField(verbose_name='提交日期', help_text='提交日期')

    class Meta:
        db_table = 'tb_overtime'
        verbose_name = '加班表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.department
