from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import math
import datetime


class PublicApiSet(viewsets.ViewSet):
    startDate = datetime.datetime(2024, 2, 26)

    @action(detail=False, methods=['get'], url_path="now_week")
    def get_now_week(self, request):
        now_data = datetime.datetime.today()
        distance = now_data - self.startDate
        now_week = math.ceil(distance.days / 7)
        print(now_week)
        return Response({'now_week': now_week}, status=status.HTTP_200_OK)
