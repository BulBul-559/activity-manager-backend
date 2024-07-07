import json
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import os
import shutil
from PIL import Image

from .models import RawPhoto, PhotoProfile, Machine


def formatTime(dt):
        return dt.strftime("%Y/%m/%d %H:%M")

def formatTimeMDHM(dt):
        return dt.strftime("%m月%d日 %H:%M")

def formatTimeMD(dt):
        return dt.strftime("%m月%d日")


def formatTimeHM(dt):
        return dt.strftime("%H:%M")


def tokenToId(request):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        # 解析 Access Token
        access_token = AccessToken(token)
        return  access_token.payload.get('sdut_id')
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Invalid token'}))


def scan_ftp_create_db_entry(machine_alias, machine_id):
    source_dir = f'ftp/{machine_alias}/'  # 源文件夹路径
    target_dir = f'final/{machine_alias}/'  # 目标文件夹路径
    thumbnail_dir = f'profile/{machine_alias}/'  # 缩略图存放路径
    result = {'status': '', 'message': ''}

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
                    path=target_path,
                    machine=Machine.objects.get(id=machine_id)
                )

                # 创建缩略图并保存到缩略图文件夹
                with Image.open(target_path) as img:
                    img.thumbnail((500, 500))
                    img.save(thumbnail_path, "JPEG", quality=95)

                # 创建新的 PhotoProfile 记录
                PhotoProfile.objects.create(
                    origin=raw_photo.id,
                    path=thumbnail_path
                )

            except Exception as e:
                result['status'] = 'Failed'
                result['message'] = f'Failed to process file {image_file}'
                return result

        result['status'] = 'Success'
        result['message'] = 'Images moved, thumbnails created, and records created'
        return result

    except Exception as e:
        result['status'] = 'Failed'
        result['message'] = str(e)
        return result