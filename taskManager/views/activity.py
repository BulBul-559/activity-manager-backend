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
from ..models import ActivityEntry


from ..serializers import ActivitySerializer
from ..serializers import MachineSerializer
from ..serializers import ActivityEntrySerializer
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


class ActivityEntryModelViewSet(viewsets.ModelViewSet):
    queryset = ActivityEntry.objects.all()
    serializer_class = ActivityEntrySerializer

    # def get_queryset(self):
    #     # 获取请求中的 user 参数
    #     machine_id = self.request.query_params.get('activity_id')
    #     # 如果 user 参数存在，则过滤 queryset
    #     if machine_id:
    #         return ActivityEntry.objects.filter(machine=machine_id)
    #     # 如果 user 参数不存在，则返回所有记录
    #     return ActivityEntry.objects.all()

    def list(self, request, *args, **kwargs):
        activity_id = request.query_params.get('activity')
        if activity_id:
            queryset = self.queryset.filter(activity_id=activity_id)
        else:
            queryset = self.queryset.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)