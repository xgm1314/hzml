from datetime import date

import django_filters.rest_framework
from django.shortcuts import render
from django.utils import timezone

# Create your views here.

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.mixins import ListModelMixin

from apps.examine.serializers import ExamineSerializer, OverTimeModelSerializer, OverTimeModifyModelSerializer
from apps.examine.models import Examine, OverTime
from utils.page import PageNum


class ExamineModelViewSet(ModelViewSet):
    # 审批视图集
    """
    list:
    查看所有审批
    create:
    新建审批
    read:
    查看单个审批
    update:
    修改审批
    delete:
    删除审批
    """
    permission_classes = [IsAdminUser]  # 权限
    queryset = Examine.objects.all().order_by('id')  # 查询集
    serializer_class = ExamineSerializer  # 序列化器
    pagination_class = PageNum  # 分页
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['department']  # 过滤
    # throttle_scope = 'a'


class OverTimeViewSet(ViewSet):
    # 加班表视图集
    permission_classes = [IsAuthenticated]
    # queryset = OverTime.objects.all().order_by('examine_id')  # 查询集
    # queryset = OverTime.objects.filter(is_delete=False)
    # serializer_class = OverTimeModelSerializer
    pagination_class = PageNum  # 分页

    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['department']  # 过滤

    def list(self, request):
        """ 获取本人所有的加班 """
        queryset = OverTime.objects.filter(name_id=request.user.id, is_delete=False)
        # 设置分页
        page_obj = PageNum()
        page_data = page_obj.paginate_queryset(queryset, request)
        # 判断该员工是否有加班数据
        if queryset.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 返回数据
        serializer = OverTimeModelSerializer(instance=page_data, context={'request': request}, many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK) # 响应没有上一页下一页的连接
        return page_obj.get_paginated_response(serializer.data)  # 响应有上一页和下一页的连接

    def create(self, request):
        """ 新建加班 """
        """
        {
            "department": "20",
            "reason": "asdfghjkl",
            "start_data": "2023-06-08 17:00:00",
            "end_data": "2023-06-08 20:00:00",
            "duration": 2,
            "examines": 1
        }
        """

        data = request.data
        serializer = OverTimeModelSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """ 查询单一加班 """
        try:
            queryset = OverTime.objects.get(examine_id=pk, is_delete=False)
        except OverTime.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            # raise ValueError('数据不存在，请检查')
        serializer = OverTimeModelSerializer(instance=queryset)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """ 修改加班信息 """
        try:
            queryset = OverTime.objects.get(examine_id=pk, is_delete=False)
            # queryset = self.get_object()
        except OverTime.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = OverTimeModifyModelSerializer(instance=queryset, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        """ 撤销加班请求 """
        try:
            queryset = OverTime.objects.get(examine_id=pk, is_delete=False)
        except OverTime.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset.is_delete = True
        queryset.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
