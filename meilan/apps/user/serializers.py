# _*_coding : uft-8 _*_
# @Time : 2023/5/18 15:11
# @Author : 
# @File : serializers
# @Project : meilan
import requests
from rest_framework import serializers
from apps.user.models import User
import re
from django.http import JsonResponse


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, label='验证码', write_only=True, required=True)
    password2 = serializers.CharField(max_length=32, write_only=True, label='确认密码')

    class Meta:
        model = User
        fields = ['id', 'password', 'password2', 'is_superuser', 'username', 'email', 'gender', 'date_joined',
                  'position', 'mobile', 'code', 'birthday', 'image', 'one_department']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'is_superuser': {
                'read_only': True
            },
            'username': {
                'max_length': 10,
                'min_length': 3
            },
            'position': {
                'max_length': 10,
                'min_length': 2
            },
            'email': {
                'required': True
            }
        }

    def validate_mobile(self, value):
        # print(value)

        result = re.match('1[345789]\d{9}', value)

        mobile = User.objects.filter(mobile=value)

        if mobile:
            raise ValueError('手机号已存在')

        if not result:
            raise ValueError('手机号格式不正确')

        return value

    def validate_email(self, value):
        # print(value)

        result = re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', value)
        # print(self.instance.pk)
        email = User.objects.filter(email=value)

        if email:
            # raise ValueError('邮箱已存在')
            return JsonResponse({'errmsg': '邮箱已注册'})

        if not result:
            # raise ValueError('邮箱格式不正确')
            return JsonResponse({'errmsg': '邮箱格式不正确'})
        return value

    def validate(self, attrs):
        # if self.validate_mobile(value=attrs.get('username')):
        #     print(1)

        # 短信验证码校验
        code = attrs.get('code')
        mobile = attrs.get('mobile')
        # print(code)
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('code')  # 连接数据库
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if not sms_code_server:
            # return JsonResponse({'code': 400, 'errmsg': '短信验证码不存在'})
            raise ValueError('短信验证码不存在')
        if code != sms_code_server.decode():
            # return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
            raise ValueError('短信验证码有误')

        # 验证密码
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password == password2:
            attrs.pop('password2')  # 删除不入库的数据
            attrs.pop('code')
            # print(attrs)
            return attrs
        else:
            raise ValueError('两次密码不一致')

    def create(self, validated_data):
        # validated_data.pop('code')
        return User.objects.create_user(**validated_data)


class UserDetailSerializer(UserSerializer):

    def validate_mobile(self, value):
        result = re.match('1[345789]\d{9}', value)
        try:
            mobile = User.objects.filter(mobile=value).values()[0]
        except Exception:
            mobile = None
        # print(mobile)
        if mobile is not None:
            user_mobile = mobile.get('username')
        else:
            user_mobile = ''
        user = str(User.objects.get(id=self.instance.pk))
        # print(mobile)
        # print(user)
        if user != user_mobile:
            if mobile:
                raise ValueError('手机号已存在')

        if not result:
            raise ValueError('手机号格式不正确')

        return value

    def validate_email(self, value):
        # print(value)
        result = re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', value)
        try:
            email = User.objects.filter(email=value).values()[0]
            # print(email)
        except Exception:
            email = None
        # print(email)
        if email is not None:
            user_email = email.get('username')
        else:
            user_email = ''

        user = str(User.objects.get(id=self.instance.pk))

        # print(username)
        # print(user)
        if user != user_email:
            # print(email)
            if email:
                # raise ValueError('邮箱已存在')
                return JsonResponse({'errmsg': '邮箱已注册'})

        if not result:
            # raise ValueError('邮箱格式不正确')
            return JsonResponse({'errmsg': '邮箱格式不正确'})

        return value

    def update(self, instance, validated_data):
        # 修改加密重写
        if 'password' in validated_data:
            password = validated_data.pop('password', None)
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginModelSerializer(serializers.ModelSerializer):
    remembered = serializers.BooleanField(label='是否记住登录', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'remembered']


"""
class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=32, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    username = serializers.CharField(max_length=10, min_length=3)
    email = serializers.EmailField(max_length=254, required=False)
    gender = serializers.ChoiceField(choices=((1, '男'), (2, '女')), required=False)
    date_joined = serializers.DateTimeField()
    position = serializers.CharField(max_length=10, min_length=2)
    mobile = serializers.CharField(max_length=11)
    birthday = serializers.DateTimeField()
    image = serializers.ImageField(allow_null=True, max_length=100, required=False)
    one_department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False)

    def validate_mobile(self, value):
        # print(value)
        result = re.match('1[345789]\d{9}', value)

        mobile = User.objects.filter(mobile=value)
        if mobile:
            raise ValueError('手机号已存在')

        if not result:
            raise ValueError('手机号格式不正确')

        return value

    def validate(self, attrs):
        # if self.validate_mobile(value=attrs.get('username')):
        #     print(1)
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password == password2:
            attrs.pop('password2')
            return attrs
        else:
            raise ValueError('两次密码不一致')

    def update(self, instance, validated_data):
        # ['id', 'password', 'password2', 'is_superuser', 'username', 'email', 'gender', 'date_joined',
        # 'position', 'mobile', 'birthday', 'image', 'one_department']
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.position = validated_data.get('position', instance.position)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.image = validated_data.get('image', instance.image)
        instance.one_department = validated_data.get('one_department', instance.one_department)
        instance.save()
        return instance
"""
