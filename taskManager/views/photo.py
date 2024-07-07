import os
import shutil
from PIL import Image

from django.http import FileResponse
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import math
import datetime
from ..models import RawPhoto, PhotoProfile, ActivityEntry
from ..serializers import RawPhotoSerializer, PhotoProfileSerializer, ActivitySerializer


class RawPhotoModelViewSet(viewsets.ModelViewSet):
    queryset = RawPhoto.objects.all()
    serializer_class = RawPhotoSerializer
    # permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[AllowAny])
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.path, 'rb'))
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoProfileModelViewSet(viewsets.ModelViewSet):
    queryset = PhotoProfile.objects.all()
    serializer_class = PhotoProfileSerializer
    # permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[AllowAny])
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.path, 'rb'))
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)