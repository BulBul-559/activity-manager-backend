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
from ..models import Machine
from ..models import PhotoProfile
from ..models import Activity
from ..models import ActivityEntry


from ..serializers import ActivitySerializer
from ..serializers import MachineSerializer
from ..serializers import ActivityEntrySerializer
from ..serializers import YoutholerSerializer

from ..utils import tokenToId, scan_ftp_create_db_entry


from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

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
            activities = Activity.objects.all().order_by('-end_time')
        else:
            # 查找 organizer 和 member 中包含这个 youtholer 的所有 Activity
            activities = Activity.objects.filter(Q(organizer=youtholer) | Q(member=youtholer)).distinct().order_by('-end_time')
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

    @action(detail=False, methods=['get'], url_path="scan")
    def scan_file(self, request):
        """
            执行活动的时候扫描FTP文件，然后创建对应的 数据库记录
            1. 扫描 FTP 文件夹（调用函数）
            2. 对比 ActivityEntry 和 RawPhoto，找出没有匹配的文件
            3. 创建 ActivityEntry 记录

            首先从 url 中获取到 machine_id，然后在 rawphoto 中寻找 name 与
            entry 中 photo_name 匹配并且machine_id与url中的machine_id相同，
            并且shoot_time与entry中的submit_time 相差不超过一周的条目才算完全匹配，
            然后再执行将entry与rawphoto与photoprofile绑定的操作
        """

        machine_id = request.query_params.get('machine_id')
        machine = Machine.objects.get(id=machine_id)
        scan_ftp_create_db_entry(machine.alias, machine_id)

        # Step 1: 查找所有 photo 为 -1 的 ActivityEntry 记录
        unbound_entries = ActivityEntry.objects.filter(photo=-1)

        # Step 2: 根据 photo_name、machine_id 和 shoot_time 进行匹配
        match = 0
        miss = 0
        for entry in unbound_entries:
            one_week_before = entry.submit_time - timedelta(weeks=1)
            one_week_after = entry.submit_time + timedelta(weeks=1)
            try:
                # 使用多条件进行匹配
                # raw_photo = RawPhoto.objects.get(
                #     Q(name__contains=entry.photo_name) &
                #     Q(machine=machine_id) &
                #     Q(shoot_time__range=(one_week_before, one_week_after))
                # )
                # shoot time 目前还没有
                raw_photo = RawPhoto.objects.get(
                    Q(name__contains=entry.photo_name) &
                    Q(machine=entry.machine)
                )
                # Step 3: 更新 ActivityEntry 的 photo 属性
                entry.photo = raw_photo.id
                entry.save()
                match += 1

            except RawPhoto.DoesNotExist:
                # 如果没有匹配的 RawPhoto，记录日志或处理异常
                miss += 1
                print(f"No matching RawPhoto found for ActivityEntry id {entry.id} with photo_name {entry.photo_name}")

        return Response({"message": "scan complete","match_count":f"{match}"},status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="key")
    def get_key(self, request):
        entry_id = request.query_params.get('entry')

        entry = ActivityEntry.objects.get(id=entry_id)

        final_key = f"青春在线-{entry.id:05}{entry.submit_time.strftime('%S')}"

        return Response({"key":final_key},status=status.HTTP_200_OK)