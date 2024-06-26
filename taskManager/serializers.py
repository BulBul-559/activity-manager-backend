from rest_framework import serializers
from .models import Sduter
from .models import Youtholer


class SduterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sduter
        fields = '__all__'

class YoutholerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtholer
        fields = '__all__'


