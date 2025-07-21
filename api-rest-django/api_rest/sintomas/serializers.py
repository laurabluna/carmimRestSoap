from rest_framework import serializers
from .models import Sintoma

class SintomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sintoma
        fields = ['id', 'sintoma1', 'sintoma2', 'sintoma3']
