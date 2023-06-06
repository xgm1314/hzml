# _*_coding : uft-8 _*_
# @Time : 2023/5/31 15:17
# @Author : 
# @File : userpermission
# @Project : meilan
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    """ 重写权限类 """
    def has_permission(self, request, view):
        # print(request.user)
        if request.user.is_superuser == 1:
            # print(request.user.is_superuser)
            return True
        return False
