from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate

# generate token and verify the token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta

import json


def SignIn(request):
    """
        Sign in the system
    """
    json_param = json.loads(request.body.decode())
    if json_param:
        username = json_param['username']
        password = json_param['password']

        user = authenticate(username=username, password=password)
        users = Sduter.objects.filter(sdut_id=username)

        if users.exists():
            users = users[0]

        if user is not None:
            # 生成 Refresh Token
            refresh = RefreshToken.for_user(user)

            refresh['sdut_id'] = user.username
            # 生成 Access Token
            access = refresh.access_token
            if users.first_login:
                return HttpResponse(
                    json.dumps({'SignState': '初次登录', 'access_token': str(access), 'refresh_token': str(refresh)}))

            # 返回 Token 值
            return HttpResponse(
                json.dumps({'SignState': '登录成功', 'access_token': str(access), 'refresh_token': str(refresh)}))
        else:
            return HttpResponse(json.dumps({'SignState': '账号或密码错误'}))
    else:
        return HttpResponse('no params')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def GetUserInfo(request):
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

        return HttpResponse(json.dumps({'sdut_id': sdut_id}))
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Invalid token'}))
