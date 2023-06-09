# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:04
# @Author : 
# @File : urls
# @Project : meilan
from django.contrib import admin
from django.urls import path

from apps.user.views import UsersModelViewSet
from apps.user.views import UsersGenericAPIView, UsersDetailGenericAPIView, LoginGenericAPIView, LogoutGenericAPIView

urlpatterns = [
    path('users/', UsersGenericAPIView.as_view()),
    path('users/<pk>/', UsersDetailGenericAPIView.as_view()),
    path('login/', LoginGenericAPIView.as_view()),
    path('logout/', LogoutGenericAPIView.as_view()),
]
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register(prefix='user', viewset=UsersModelViewSet, basename='users')
urlpatterns += router.urls
