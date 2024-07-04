import json
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

def formatTime(dt):
        return dt.strftime("%Y/%m/%d %H:%M")

def formatTimeMDHM(dt):
        return dt.strftime("%m月%d日 %H:%M")

def formatTimeMD(dt):
        return dt.strftime("%m月%d日")


def formatTimeHM(dt):
        return dt.strftime("%H:%M")


def tokenToId(request):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        # 解析 Access Token
        access_token = AccessToken(token)
        return  access_token.payload.get('sdut_id')
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Invalid token'}))
