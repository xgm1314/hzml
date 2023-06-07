# _*_coding : uft-8 _*_
# @Time : 2023/5/31 20:20
# @Author : 
# @File : exceptions
# @Project : meilan
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response

from django.db import DatabaseError


def exception_handler(exc, context):
    """ 在DRF的异常捕获基础增加数据库的异常捕获 """
    response = drf_exception_handler(exc, context)
    if response:
        return response
    view = context['view']
    if isinstance(exc, DatabaseError):
        print('[%s]:%s' % (view, exc))
        response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return response

    return None
