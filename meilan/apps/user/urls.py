# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:04
# @Author : 
# @File : urls
# @Project : meilan
from django.contrib import admin
from django.urls import path

# from apps.user.views import UsersModelViewSet
from apps.user.views import UsersGenericAPIView, UsersDetailGenericAPIView

urlpatterns = [
    path('users/', UsersGenericAPIView.as_view()),
    path('users/<pk>/', UsersDetailGenericAPIView.as_view()),
]
# from rest_framework.routers import SimpleRouter
#
# router = SimpleRouter()
# router.register(prefix='users', viewset=UsersModelViewSet, basename='users')
# urlpatterns += router.urls
