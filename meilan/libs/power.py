# _*_coding : uft-8 _*_
# @Time : 2023/5/24 12:39
# @Author : 
# @File : power
# @Project : meilan
from rest_framework import permissions

from apps.user.models import User


class UserBasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if_staff = request.META['if_staff']
        users = User.objects.filter(id=if_staff).exists()
        return not users
