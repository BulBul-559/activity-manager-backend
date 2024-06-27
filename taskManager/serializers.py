from rest_framework import serializers
from .models import Sduter
from .models import Youtholer
from .models import Machine
from .models import MachineAlloc
from .models import Task
from .models import RawPhoto
from .models import PhotoProfile
from .models import FinalPhoto


class SduterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sduter
        fields = '__all__'


class YoutholerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtholer
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Machine
        fields = '__all__'


class MachineAllocSerializer(serializers.ModelSerializer):

    class Meta:
        model = MachineAlloc
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class RawPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RawPhoto
        fields = '__all__'

class PhotoProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoProfile
        fields = '__all__'

class FinalPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalPhoto
        fields = '__all__'
