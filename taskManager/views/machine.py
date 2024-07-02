from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse

from ..models import Youtholer
from ..models import Machine
from ..models import MachineBorrowRecord
from ..models import MachineBorrowHistory

from ..serializers import MachineSerializer
from ..serializers import MachineBorrowRecordSerializer
from ..serializers import MachineBorrowHistorySerializer

from intervaltree import IntervalTree

class MachineModelViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    @action(methods=['get', 'post'], detail=True, permission_classes=[AllowAny])
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.profile.path, 'rb'))
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MachineBorrowViewSet(viewsets.ModelViewSet):
    queryset = MachineBorrowRecord.objects.all()
    serializer_class = MachineBorrowRecordSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # 获取请求中的 user 参数
        machine_id = self.request.query_params.get('machine_id')
        # 如果 user 参数存在，则过滤 queryset
        if machine_id:
            return MachineBorrowRecord.objects.filter(machine=machine_id)
        # 如果 user 参数不存在，则返回所有记录
        return MachineBorrowRecord.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data

            return self.get_paginated_response({'data': data})

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for i in data:
            youthol = Youtholer.objects.get(id=i['youtholer'])
            i['borrower'] = youthol.name

        return Response(data, status=status.HTTP_200_OK)

    # def list(self, request, *args, **kwargs):
    #     # 重写 GET 方法
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     # 重写 GET 方法以获取单个记录
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            borrow_time = serializer.validated_data['borrow_time']
            finish_time = serializer.validated_data['finish_time']
            machine_id = serializer.validated_data['machine'].id

            # 获取当前机器的所有借用记录
            busy_list = MachineBorrowRecord.objects.filter(
                machine_id=machine_id,
                finish_time__gt=borrow_time,
                borrow_time__lt=finish_time
            )

            # 使用 IntervalTree 判断时间段重叠
            busy_time = IntervalTree()
            for item in busy_list:
                busy_time[item.borrow_time.timestamp():item.finish_time.timestamp()] = item.id

            if busy_time.overlap(borrow_time.timestamp(), finish_time.timestamp()):
                return Response({'detail': '设备在该时间段内已经被借用'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)