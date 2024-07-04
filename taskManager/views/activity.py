from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q

from ..models import Youtholer
from ..models import Machine
from ..models import Activity

from ..serializers import MachineSerializer
from ..serializers import ActivitySerializer
from ..serializers import YoutholerSerializer

from ..utils import tokenToId

from intervaltree import IntervalTree
from datetime import datetime


class ActivityModelViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


def list(self, request, *args, **kwargs):
    sdut_id = tokenToId(request)
    if isinstance(sdut_id, HttpResponse):  # 如果 tokenToId 返回的是 HttpResponse，说明 token 无效
        return sdut_id

    youtholer = Youtholer.objects.filter(sdut_id=sdut_id).first()
    if not youtholer:
        return Response({'error': 'Youtholer not found'}, status=status.HTTP_404_NOT_FOUND)

    # 如果是站长、部长或副部长，则返回全部数据
    if youtholer.position in ['站长', '部长', '副部长']:
        activities = Activity.objects.all()
    else:
        # 查找 organizer 和 member 中包含这个 youtholer 的所有 Activity
        activities = Activity.objects.filter(Q(organizer=youtholer) | Q(member=youtholer)).distinct()

    page = self.paginate_queryset(activities)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(activities, many=True)
    return Response(serializer.data)