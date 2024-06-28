from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
# generate token and verify the token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta

from .utils import tokenToId
import json

from .models import Sduter
from .models import Youtholer

from .serializers import YoutholerSerializer
def Create(request):
    """
        Sign up to the system.
        Here just a simple example.
    """
    username = 'sunorain'
    password = 'youthol'
    email = "1079729701@qq.com"
    User.objects.create_user(username, email, password)

    sdut_id = 'sunorain'
    name = '小悠'
    college = '山东理工大学'
    grade = '214'
    identity = '学生'
    sduter = Sduter.objects.create(sdut_id=sdut_id, name=name, college=college,
                                    grade=grade,identity = identity)
    department = '管理组'
    identity = '管理员'
    youtholer = Youtholer.objects.create(origin_info=sduter, sdut_id=sdut_id, name=name, department=department, identity=identity)
    youtholer.save()

    return HttpResponse('success')


class AccountApiSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sign_in(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            users = Sduter.objects.filter(sdut_id=username)[0]

            refresh = RefreshToken.for_user(user)
            refresh['sdut_id'] = user.username

            access = refresh.access_token

            response_data = {
                'message': 'Login successful',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }

            if users.first_login:
                response_data['sign_state'] = '初次登录'
            else:
                response_data['sign_state'] = '登录成功'
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials', 'sign_state': '账号或密码错误'},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path="change")
    def change_password(self, request):
        request_data = request.data

        username = tokenToId(request)
        password = request_data['password']

        user = authenticate(username=username, password=password)
        users = Sduter.objects.filter(sdut_id=username)[0]

        if user is not None:

            refresh = RefreshToken.for_user(user)
            refresh['sdut_id'] = user.username
            access = refresh.access_token

            new_pwd = request_data['new_pwd']
            again_pwd = request_data['again_pwd']
            if new_pwd != again_pwd:
                response_data = {'message': '两次密码不一致'}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)
            user.set_password(new_pwd)
            user.save()

            if 'first_login' in request_data:
                users.first_login = False
                users.save()

            response_data = {
                'message': '修改成功',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {'message': '原密码错误'}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="info")
    def get_info(self, request):
        """
            Verify the token and return the user basic infomation.
            1. sdut_id (same as username)
        """
        # 只有经过身份验证的用户才能访问此视图
        # 获取用户的基本信息
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            # 解析 Access Token
            access_token = AccessToken(token)
            # 获取用户信息
            sdut_id = access_token.payload.get('sdut_id')
            # 在这里查询其他的信息并返回
            return Response({'sdut_id': sdut_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path="youtholer")
    def get_youtholer(self, request):
        """
            Verify the token and return the user basic infomation.
            1. sdut_id (same as username)

        """
        # 只有经过身份验证的用户才能访问此视图
        # 获取用户的基本信息
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            # 解析 Access Token
            access_token = AccessToken(token)
            # 获取用户信息
            sdut_id = access_token.payload.get('sdut_id')
            youthol = Youtholer.objects.filter(sdut_id=sdut_id)[0]


            if not youthol:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = YoutholerSerializer(youthol)

            response_data = {
                'message': "获取信息成功",
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)