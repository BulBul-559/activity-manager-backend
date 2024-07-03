from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Youtholer
from ..models import Sduter


from ..serializers import YoutholerSerializer


class YoutholerModelViewSet(viewsets.ModelViewSet):
    queryset = Youtholer.objects.all()
    serializer_class = YoutholerSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path="add-one")
    def add_one_user(self, request):
        sdut_id = request.data.get('sdut_id')
        name = request.data.get('name')
        college = request.data.get('college')
        grade = request.data.get('grade')
        identity = request.data.get('identity')
        department = request.data.get('department')
        position = request.data.get('position', '成员')

        if sdut_id is None or name is None or college is None or grade is None or identity is None or department is None:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断 user 中有没有
        if not User.objects.filter(username=sdut_id).exists():
            user = User.objects.create_user(sdut_id, f"{sdut_id}@stumail.sdut.edu.cn", 'youthol')
            user.save()

        # 判断 sduter 中有没有
        if not Sduter.objects.filter(sdut_id=sdut_id).exists():
            sduter = Sduter.objects.create(
                sdut_id=sdut_id,
                name=name,
                college=college,
                grade=grade,
                identity='学生'
            )
            sduter.save()
        else:
            sduter = Sduter.objects.get(sdut_id=sdut_id)

        # 判断 youtholer 中有没有
        if not Youtholer.objects.filter(sdut_id=sdut_id, department=department).exists():
            youtholer = Youtholer.objects.create(
                origin_info=sduter,
                sdut_id=sdut_id,
                name=name,
                department=department,
                identity=identity,
                position=position
            )
            youtholer.save()


        return Response({'message': '添加成功'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        sduter = instance.origin_info

        data = {
            'id': instance.id,
            'sdut_id': sduter.sdut_id,
            'name': sduter.name,
            'college': sduter.college,
            'grade': sduter.grade,
            'identity': instance.identity,  # 使用 Youtholer 的 identity
            'phone': sduter.phone,
            'qq_number': sduter.qq_number,
            'birthday': sduter.birthday,
            'first_login': sduter.first_login,
            'department': instance.department,
            'position': instance.position,
        }

        return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        result_list = []

        for youtholer in queryset:
            sduter = youtholer.origin_info

            data = {
                'id': youtholer.id,
                'sdut_id': sduter.sdut_id,
                'name': sduter.name,
                'college': sduter.college,
                'grade': sduter.grade,
                'identity': youtholer.identity,  # 使用 Youtholer 的 identity
                'phone': sduter.phone,
                'qq_number': sduter.qq_number,
                'birthday': sduter.birthday,
                'first_login': sduter.first_login,
                'department': youtholer.department,
                'position': youtholer.position,
            }
            result_list.append(data)

        return Response(result_list, status=status.HTTP_200_OK)
