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
from .models import Machine

from .serializers import YoutholerSerializer
from .serializers import MachineSerializer
from django.http import FileResponse

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

