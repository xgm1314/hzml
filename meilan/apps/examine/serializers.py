# _*_coding : uft-8 _*_
# @Time : 2023/6/7 14:18
# @Author : 
# @File : serializers
# @Project : meilan

# from django.utils import timezone
import datetime
from datetime import *

from rest_framework import serializers
from rest_framework.response import Response
from apps.examine.models import Examine, OverTime
from apps.department.models import Department
from datetime import *


class ExamineSerializer(serializers.ModelSerializer):
    # 审批序列化器
    # department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    # department = serializers.StringRelatedField(label='部门',required=False)
    # one_examine = serializers.StringRelatedField(label='一级审批', required=False)
    # two_examine = serializers.StringRelatedField(label='二级审批', required=False)
    # three_examine = serializers.StringRelatedField(label='三级审批', required=False)
    # four_examine = serializers.StringRelatedField(label='四级审批', required=False)
    # five_examine = serializers.StringRelatedField(label='五级审批', required=False)
    # one_copy = serializers.StringRelatedField(label='抄送人1', required=False)
    # two_copy = serializers.StringRelatedField(label='抄送人2', required=False)
    # three_copy = serializers.StringRelatedField(label='抄送人3', required=False)
    # four_copy = serializers.StringRelatedField(label='抄送人4', required=False)
    # five_copy = serializers.StringRelatedField(label='抄送人5', required=False)

    class Meta:
        model = Examine
        fields = '__all__'


class OverTimeModelSerializer(serializers.ModelSerializer):
    # 加班序列化器
    name = serializers.StringRelatedField(label='提交人')

    class Meta:
        model = OverTime
        exclude = ['is_delete', '_data']  # 排除这个字段
        read_only = ['examine_id', 'examines']
        extra_kwargs = {
            'examine_id': {
                'read_only': True
            },
            'data': {
                'read_only': True,
                'required': False
            },
            'reason': {
                'max_length': 100,
                'min_length': 2
            }
        }

    # def get_name(self, obj):
    #     # 添加登录用户的数据信息
    #     # user = self.context['request'].user
    #     # return obj.is_flavor(user.username)
    #     return self.context['request'].user.username

    def validate(self, attrs):
        start_data = attrs.get('start_data')
        end_data = attrs['end_data']
        # start_data_time = datetime.strptime(start_data, '%Y-%m-%d %H:%M:%S')
        # end_data_time = datetime.strptime(end_data, '%Y-%m-%d %H:%M:%S')
        if start_data == '':
            raise ValueError('请输入起始时间')
        if end_data == '':
            raise ValueError('请输入结束时间')
        day_time = (end_data - start_data).days
        second_time = (end_data - start_data).seconds
        if day_time < 0:
            raise ValueError('输入有误')

        attrs['data'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        attrs['_data'] = date.today()
        attrs['name'] = self.context['request'].user
        # id = 1
        # if OverTime.objects.filter(_data=date.today()).count() < 1:
        #     id = id
        # else:
        #     id = id + 1

        # if OverTime.objects.filter(_data=date.today()).count() < 1:
        for id in range(1, 99999):
            examine_id = datetime.now().strftime('%Y%m%d') + '%05d' % id
            if OverTime.objects.filter(examine_id=examine_id).count() == 0:
                attrs['examine_id'] = examine_id
                break
            else:
                id += 1

        return attrs
        # if second_time >= 60 * 60:
        #     hours = divmod(second_time, 60 * 60)
        #     if hours[1] >= 60:
        #         mins = divmod(hours[1], 60)
        #         return Response('%s小时%s分钟' % (int(day_time) * 24 + hours[0], mins[0]))
        #     elif second_time >= 60:
        #         mins = divmod(second_time, 60)
        #         return Response('%s小时%s分钟' % (int(day_time) * 24, mins[0]))


class OverTimeModifyModelSerializer(OverTimeModelSerializer):

    def validate(self, attrs):
        start_data = attrs.get('start_data')
        end_data = attrs['end_data']
        # start_data_time = datetime.strptime(start_data, '%Y-%m-%d %H:%M:%S')
        # end_data_time = datetime.strptime(end_data, '%Y-%m-%d %H:%M:%S')
        if start_data == '':
            raise ValueError('请输入起始时间')
        if end_data == '':
            raise ValueError('请输入结束时间')
        day_time = (end_data - start_data).days
        second_time = (end_data - start_data).seconds
        if day_time < 0:
            raise ValueError('输入有误')

        attrs['data'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        attrs['_data'] = date.today()

        return attrs
