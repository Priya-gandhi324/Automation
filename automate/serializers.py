from rest_framework import serializers
from .models import Courts, Total


class CourtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courts
        fields = '__all__'


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = '__all__'
