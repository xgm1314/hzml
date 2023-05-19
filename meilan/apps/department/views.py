import json

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

class OneDepartmentModelViewSet(GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = OneDepartmentSerializer
    def get(self, request):
        # 查看所有部门
        departments = Department.objects.all()
        serializer = OneDepartmentSerializer(instance=departments, many=True)
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 添加部门
        data = request.data
        serializer = OneDepartmentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TwoDepartmentModelViewSet(GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = OneDepartmentSerializer

    def get(self, request, pk):
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
        two_department = self.get_object()
        data = request.data
        serializer = OneDepartmentSerializer(instance=two_department, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return JsonResponse({'code': 0, 'errmsg': serializer.data})
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        two_department = self.get_object()
        two_department.delete()
        # return JsonResponse({'code': 204, 'errmsg': 'ok'})
        return Response(status=status.HTTP_204_NO_CONTENT)
