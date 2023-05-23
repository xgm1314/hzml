from django.shortcuts import render

# Create your views here.
from apps.user.serializers import UserSerializer, UserDetailSerializer
from apps.user.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from utils.page import PageNum

"""
class UsersModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""


class UsersGenericAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    pagination_class = PageNum

    def get(self, request):
        # 查看所有员工
        user = self.get_queryset()
        project_qs = self.filter_queryset(user)
        # print(project_qs)
        page = self.paginate_queryset(project_qs)
        # print(page)
        if page:
            serializer_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        serializer = self.serializer_class(instance=user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 添加员工
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UsersDetailGenericAPIView(GenericAPIView):
    # pagination_class = PageNum
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'

    def get(self, request, pk):
        user = self.get_object()
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user_dict = self.get_object()
        data = request.data

        serializer = self.serializer_class(instance=user_dict, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
