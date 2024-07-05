from rest_framework import serializers
from .models import Sduter
from .models import Youtholer
from .models import Machine
from .models import MachineBorrowRecord
from .models import Activity
from .models import RawPhoto
from .models import FinalPhoto
from .models import PhotoProfile
from django.urls import reverse

class SduterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sduter
        fields = '__all__'


class YoutholerSerializer(serializers.ModelSerializer):
    origin_info = serializers.PrimaryKeyRelatedField(queryset=Sduter.objects.all())

    class Meta:
        model = Youtholer
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = '__all__'
        # exclude = ['profile']

    def get_profile_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        # 构建下载 URL
        return request.build_absolute_uri(reverse('machine-download', args=[obj.pk]))


class MachineBorrowRecordSerializer(serializers.ModelSerializer):
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    youtholer = serializers.PrimaryKeyRelatedField(queryset=Youtholer.objects.all())

    class Meta:
        model = MachineBorrowRecord
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    organizer = YoutholerSerializer(read_only=True)
    organizer_id = serializers.PrimaryKeyRelatedField(queryset=Youtholer.objects.all(), source='organizer', write_only=True)
    member = YoutholerSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(queryset=Youtholer.objects.all(), many=True, write_only=True, source='member')

    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        members_data = validated_data.pop('member')
        task = Activity.objects.create(**validated_data)
        task.member.set(members_data)
        return task

    def update(self, instance, validated_data):
        members_data = validated_data.pop('member')
        instance.name = validated_data.get('name', instance.name)
        instance.organizer = validated_data.get('organizer', instance.organizer)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.is_valid = validated_data.get('is_valid', instance.is_valid)
        instance.save()

        instance.member.set(members_data)
        return instance



class RawPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = RawPhoto
        fields = '__all__'

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        # 构建下载 URL
        return request.build_absolute_uri(reverse('rawphoto-download', args=[obj.pk]))



class PhotoProfileSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = PhotoProfile
        fields = '__all__'

    def get_profile_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        # 构建下载 URL
        return request.build_absolute_uri(reverse('photoprofile-download', args=[obj.pk]))


class FinalPhotoSerializer(serializers.ModelSerializer):
    origin = RawPhotoSerializer(read_only=True)  # 嵌套的 RawPhoto 序列化器
    origin_id = serializers.PrimaryKeyRelatedField(queryset=RawPhoto.objects.all(), source='origin', write_only=True)
    uploader = YoutholerSerializer(read_only=True)  # 嵌套的 Youtholer 序列化器
    uploader_id = serializers.PrimaryKeyRelatedField(queryset=Youtholer.objects.all(), source='uploader', write_only=True)

    class Meta:
        model = FinalPhoto
        fields = '__all__'
