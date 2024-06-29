from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from ..models import Machine

from ..serializers import MachineSerializer
from django.http import FileResponse

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
        return Response(serializer.data)
