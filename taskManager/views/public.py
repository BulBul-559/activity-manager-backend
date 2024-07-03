from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import math
import datetime


class PublicApiSet(viewsets.ViewSet):
    startDate = datetime.datetime(2024, 2, 26)

    @action(detail=False, methods=['get'], url_path="current-week")
    def get_now_week(self, request):
        now_data = datetime.datetime.today()
        distance = now_data - self.startDate
        now_week = math.ceil(distance.days / 7)
        print(now_week)
        return Response({'current_week': now_week}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="college-list")
    def get_college_list(self, request):
        colleges = [
            "机械工程学院",
            "交通与车辆工程学院",
            "农业工程与食品科学学院",
            "电气与电子工程学院",
            "计算机科学与技术学院",
            "化学化工学院",
            "建筑工程与空间信息学院",
            "资源与环境工程学院",
            "材料科学与工程学院",
            "生命与医药学院",
            "数学与统计学院",
            "物理与光电工程学院",
            "经济学院",
            "管理学院",
            "文学与新闻传播学院",
            "外国语学院",
            "法学院",
            "马克思主义学院",
            "美术学院",
            "音乐学院",
            "鲁泰纺织服装学院"
        ]
        return Response(colleges, status=status.HTTP_200_OK)