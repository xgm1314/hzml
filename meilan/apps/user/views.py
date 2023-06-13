import re

import django_filters
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_filters import filters

from rest_framework.throttling import UserRateThrottle

from apps.user.serializers import UserSerializerRoot, UserSerializerOrdinary, UserDetailSerializerRoot, \
    LoginModelSerializer
from apps.user.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.filters import OrderingFilter  # 排序
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from utils.page import PageNum

from django.http import JsonResponse
from django.views import View


class UsersModelViewSet(ModelViewSet):
    # 员工视图
    """
    list:
    查看所有员工
    create:
    新建员工
    read:
    查看单个员工
    update:
    修改员工
    delete:
    删除员工
    """
    # queryset = User.objects.all()
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializerRoot

    # 指定认证方式，判断用户是否已经成功登录
    # authentication_classes = [JWTAuthentication, BasicAuthentication]
    # 根据用户权限来限制访问
    permission_classes = [IsAuthenticated, IsAdminUser]

    # from rest_framework.throttling import AnonRateThrottle
    # throttle_classes = [AnonRateThrottle]

    throttle_scope = 'a'  # 限流，配置未成功

    # from rest_framework.filters import OrderingFilter
    # filter_backends = [OrderingFilter]  # 排序
    # ordering_fields = ['username', 'email', 'id', 'date_joined']

    # from django_filters.rest_framework import DjangoFilterBackend
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # django_filter过滤器
    filterset_fields = ['username', 'position', 'mobile', 'one_department', 'id']  # django_filter过滤器

    pagination_class = PageNum


# @csrf_exempt
class LoginGenericAPIView(APIView):
    """ 用户登录 """
    throttle_scope = 'a'

    """
    {
    "username":"admin@qq.com",
    "password":"123456",
    "remembered":"True"
    }
    """

    # queryset = User.objects.all()
    # serializer_class = LoginModelSerializer

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
            # return JsonResponse({'code': 400, 'errmsg': '参数不全'})
            return Response(status=status.HTTP_404_NOT_FOUND)
        from django.contrib.auth import authenticate
        users = authenticate(username=username, password=password)
        if users is None:
            # return JsonResponse({'code': 400, 'errmsg': '用户名或者密码不正确'})
            return Response(status=status.HTTP_404_NOT_FOUND)
        from django.contrib.auth import login
        login(request, users)
        if remembered:
            request.session.set_expiry(60 * 60 * 24 * 7)  # 将用户信息写入session中
        else:
            request.session.set_expiry(0)
        # response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie('username', username)
        return response


class LogoutGenericAPIView(APIView):
    """ 用户退出 """

    def delete(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('username')
        return response


from utils.userpermission import UserPermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UsersGenericAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # # permission_classes = [UserPermission]
    # permission_classes = [IsAuthenticated]
    # # queryset = User.objects.all()

    """
    添加order_by()可解决问题或者在models添加排序ordering = ['id']
    UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'apps.user.models.User'> QuerySet.
    paginator = self.django_paginator_class(queryset, page_size)
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializerRoot
    # print(serializer_class)

    pagination_class = PageNum

    from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
    throttle_scope = 'a'  # 限流未配置成功
    throttle_classes = (AnonRateThrottle,)

    # from rest_framework.filters import OrderingFilter
    # filter_backends = [OrderingFilter]  # 排序
    # ordering_fields = ['username', 'email', 'id', 'date_joined']

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # django_filter过滤器
    filterset_fields = ['username', 'position', 'mobile', 'one_department', 'id']  # django_filter过滤器

    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return UserSerializerRoot
    #     else:
    #         return UserSerializerOrdinary

    def get(self, request):
        """查看所有员工"""

        # from django.db import DatabaseError
        # raise DatabaseError('数据库异常')  # 抛异常测试,未成功

        user = self.get_queryset()
        project_qs = self.filter_queryset(user)
        # print(project_qs)
        page = self.paginate_queryset(project_qs)
        # print(page)

        if page:
            serializer_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer_obj.data)
        # serializer = self.serializer_class(instance=user, many=True)

        serializer = self.get_serializer(instance=user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ 添加员工 """
        """
        {
        "password":123456,
        "password2":123456,
        "username":"admin06",
        "email":"admin06@qq.com",
        "gender":2,
        "position":"电工",
        "mobile":17854157598,
        "code":6339,
        "one_department":6
        }
        """
        data = request.data
        # mobile = data.get('mobile')  # 获取前端传入的手机号
        # print(data)
        serializer = UserSerializerRoot(data=data)
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


from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework


class UsersDetailGenericAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # pagination_class = PageNum
    queryset = User.objects.all()
    serializer_class = UserDetailSerializerRoot

    lookup_field = 'pk'

    def get(self, request, pk):
        """查看一个员工"""
        user = self.get_object()
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """修改员工"""
        user_dict = self.get_object()
        data = request.data

        serializer = self.serializer_class(instance=user_dict, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """删除员工"""
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
