# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:04
# @Author : 
# @File : urls
# @Project : meilan
from django.contrib import admin
from django.urls import path
from apps.examine.views import ExamineModelViewSet, OverTimeViewSet

from rest_framework.routers import SimpleRouter, DefaultRouter

urlpatterns = [

]
router = DefaultRouter()
router.register(prefix='examines', viewset=ExamineModelViewSet, basename='examines')
router.register(prefix='overtime', viewset=OverTimeViewSet, basename='overtime')
urlpatterns += router.urls
