from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q

from ..models import Youtholer
from ..models import RawPhoto
from ..models import PhotoProfile
from ..models import Activity
from ..models import ActivityEntry


from ..serializers import ActivitySerializer
from ..serializers import MachineSerializer
from ..serializers import ActivityEntrySerializer
from ..serializers import YoutholerSerializer

from ..utils import tokenToId, scan_ftp_create_db_entry

from intervaltree import IntervalTree
from datetime import datetime
import re


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
        activity_id = request.query_params.get('activity_id')
        if activity_id:
            queryset = self.queryset.filter(activity_id=activity_id).order_by('-submit_time')
        else:
            queryset = self.queryset.all().order_by('-submit_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityEntryViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path="scan")
    def scan_file(self, request):
        """
            执行活动的时候扫描FTP文件，然后创建对应的 数据库记录
            1. 扫描 FTP 文件夹（调用函数）
            2. 对比 ActivityEntry 和 RawPhoto，找出没有匹配的文件
            3. 创建 ActivityEntry 记录
        """

        machine_alias = request.query_params.get('machine_alias')
        scan_ftp_create_db_entry(machine_alias)

        machine_alias = request.query_params.get('machine_alias')
        scan_ftp_create_db_entry(machine_alias)

        # Step 1: 查找所有 photo 为 -1 的 ActivityEntry 记录
        unbound_entries = ActivityEntry.objects.filter(photo=-1)

        # Step 2: 根据 photo_name 部分匹配 RawPhoto
        for entry in unbound_entries:
            try:
                # 使用 __contains 进行部分匹配
                raw_photo = RawPhoto.objects.get(name__contains=entry.photo_name)

                # Step 3: 更新 ActivityEntry 的 photo 属性
                entry.photo = raw_photo.id
                entry.save()

                # 创建 PhotoProfile
                photo_profile = PhotoProfile(origin=raw_photo.id, path=raw_photo.path)
                photo_profile.save()

            except RawPhoto.DoesNotExist:
                # 如果没有匹配的 RawPhoto，记录日志或处理异常
                print(f"No matching RawPhoto found for ActivityEntry id {entry.id} with photo_name {entry.photo_name}")

        return Response({"status": "scan complete"})