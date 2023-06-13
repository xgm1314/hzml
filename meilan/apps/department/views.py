import json

import django_filters
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from apps.department.serializers import OneDepartmentSerializer
from apps.department.models import Department
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from utils.page import PageNum,LimitNum


# from rest_framework.pagination import PageNumberPagination


# Create your views here.

# class OneDepartmentModelViewSet(ModelViewSet):
#     queryset = Department.objects.all()
#     serializer_class = OneDepartmentSerializer
#
#     def get(self, request):
#
#         department = Department.objects.filter(Superior=None)  # 获取省份对象
#         province_list = []  # 定义空列表
#         for province in department:
#             province_list.append({
#                 'id': province.id,
#                 'name': province.name
#             })
#         # serializer = OneDepartmentSerializer(instance=province_list, many=True)  # 将对象数据转化为字典数据
#         # return JsonResponse({'code': 0, 'books': serializer.data})
#         return Response(data=province_list, status=status.HTTP_200_OK)


class OneDepartmentGenericAPIView(GenericAPIView):
    pagination_class = PageNum
    # pagination_class = LimitNum
    permission_classes = [AllowAny]
    queryset = Department.objects.all().order_by('id')
    serializer_class = OneDepartmentSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # django_filter过滤器
    filterset_fields = ['name', 'id']  # django_filter过滤器

    # from rest_framework.filters import OrderingFilter
    # filter_backends = [OrderingFilter]  # django_filter排序
    # ordering_fields = ['name', 'id']  # django_filter排序

    def get(self, request):
        """查看所有部门"""
        departments = self.get_queryset()
        project_qs = self.filter_queryset(departments)
        # print(project_qs)
        page = self.paginate_queryset(project_qs)
        # print(page)
        if page:
            serializer_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)

        serializer = OneDepartmentSerializer(instance=departments, many=True)
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """添加部门"""
        data = request.data
        serializer = OneDepartmentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TwoDepartmentGenericAPIView(GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = OneDepartmentSerializer

    def get(self, request, pk):
        """ 查看一个部门 """
        two_department = self.get_object()
        serializer = self.serializer_class(instance=two_department)
        serializer_data = serializer.data
        # print(serializer_data)
        three_department = two_department.subs.all()
        # print(three_department)
        data_list = []
        data_list.append({'id': pk, 'name': serializer_data.get('name')})

        for item in three_department:
            data_list.append({
                'id': item.id,
                'name': item.name
            })
        # return JsonResponse({'code': 0, 'errmsg': data_list})
        return Response(data=data_list, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """ 修改部门 """
        two_department = self.get_object()
        data = request.data
        serializer = OneDepartmentSerializer(instance=two_department, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """ 删除部门 """
        two_department = self.get_object()
        two_department.delete()
        # return JsonResponse({'code': 204, 'errmsg': 'ok'})
        return Response(status=status.HTTP_204_NO_CONTENT)
