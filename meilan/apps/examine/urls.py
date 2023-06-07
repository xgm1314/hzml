# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:04
# @Author : 
# @File : urls
# @Project : meilan
from django.contrib import admin
from django.urls import path
from apps.department.views import OneDepartmentGenericAPIView
from apps.department.views import TwoDepartmentGenericAPIView
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('department/', OneDepartmentGenericAPIView.as_view()),
    path('department/<pk>/', TwoDepartmentGenericAPIView.as_view())
]
# router = SimpleRouter()
# router.register(prefix='department', viewset=OneDepartmentModelViewSet, basename='department')
# urlpatterns += router.urls
