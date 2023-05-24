import re

from django.shortcuts import render

# Create your views here.
from apps.user.serializers import UserSerializer, UserDetailSerializer, LoginModelSerializer
from apps.user.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from utils.page import PageNum

from django.http import JsonResponse
from django.views import View

"""
class UsersModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
"""


class LoginGenericAPIView(GenericAPIView):
    """ 用户登录 """
    """
    {
    "username":"admin@qq.com",
    "password":"123456",
    "remembered":"True"
    }
    """
    queryset = User.objects.all()
    serializer_class = LoginModelSerializer

    def post(self, request):
        user = request.data
        username = user.get('username')
        password = user.get('password')
        remembered = user.get('remembered')
        if re.match('1[345789]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        if re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', username):
            User.USERNAME_FIELD = 'email'
        else:
            User.USERNAME_FIELD = 'username'
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        from django.contrib.auth import authenticate
        users = authenticate(username=username, password=password)
        if users is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或者密码不正确'})
        from django.contrib.auth import login
        login(request, users)
        if remembered:
            request.session.set_expiry(60 * 60 * 24 * 7)  # 将用户信息写入session中
        else:
            request.session.set_expiry(0)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username)
        return response


class LogoutGenericAPIView(View):
    """ 用户退出 """

    def delete(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')
        return response


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
        # mobile = data.get('mobile')  # 获取前端传入的手机号
        # print(data)
        serializer = UserSerializer(data=data)
        # print(serializer)

        # # 短信验证码校验
        # code = data.get('code')
        # mobile = data.get('mobile')
        # # print(code)
        # from django_redis import get_redis_connection
        # redis_conn = get_redis_connection('code')  # 连接数据库
        # sms_code_server = redis_conn.get('sms_%s' % mobile)
        # if not sms_code_server:
        #     return JsonResponse({'code': 400, 'errmsg': '短信验证码不存在'})
        # if code != sms_code_server.decode():
        #     return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

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
