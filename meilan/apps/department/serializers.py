# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:11
# @Author : 
# @File : serializers
# @Project : meilan
from rest_framework import serializers
from apps.department.models import Department


class OneDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'max_length': 20,
                'min_length': 3
            }
        }

