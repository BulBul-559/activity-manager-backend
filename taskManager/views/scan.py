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
from ..models import RawPhoto, PhotoProfile
from ..serializers import RawPhotoSerializer, PhotoProfileSerializer


class ScanViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path="scan")
    def scan_and_move(self, request, format=None):
        source_dir = 'ftp/a73/'  # 源文件夹路径
        target_dir = 'final/a73/'  # 目标文件夹路径
        thumbnail_dir = 'profile/a73/'  # 缩略图存放路径

        try:
            # 检查目标文件夹和缩略图文件夹是否存在，不存在则创建
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            if not os.path.exists(thumbnail_dir):
                os.makedirs(thumbnail_dir)

            # 扫描源文件夹中的所有图片文件
            image_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

            for image_file in image_files:
                source_path = os.path.join(source_dir, image_file)
                target_path = os.path.join(target_dir, image_file)
                thumbnail_path = os.path.join(thumbnail_dir, image_file)

                try:
                    # 移动文件到目标文件夹
                    shutil.move(source_path, target_path)

                    # 创建新的 RawPhoto 记录
                    raw_photo = RawPhoto.objects.create(
                        name=image_file,
                        path=target_path
                    )

                    # 创建缩略图并保存到缩略图文件夹
                    with Image.open(target_path) as img:
                        img.thumbnail((200, 200))
                        img.save(thumbnail_path, "JPEG", quality=85)

                    # 创建新的 PhotoProfile 记录
                    PhotoProfile.objects.create(
                        origin=raw_photo.id,
                        path=thumbnail_path
                    )

                except Exception as e:
                    # logger.error(f"Failed to process file {image_file}: {e}")
                    return Response({'status': 'Failed', 'message': f'Failed to process file {image_file}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'status': 'Images moved, thumbnails created, and records created'}, status=status.HTTP_200_OK)

        except Exception as e:
            # logger.error(f"Error occurred during scan and move: {e}")
            return Response({'status': 'Failed', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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