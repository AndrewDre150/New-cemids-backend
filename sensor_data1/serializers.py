from rest_framework import serializers
from .models import SensorData1

class SensorData1Serializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData1
        fields = '__all__'
