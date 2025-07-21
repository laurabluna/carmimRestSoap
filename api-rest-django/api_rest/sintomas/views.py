from django.shortcuts import render
from rest_framework import viewsets
from .models import Sintoma
from .serializers import SintomaSerializer

class SintomaViewSet(viewsets.ModelViewSet):
    queryset = Sintoma.objects.all()
    serializer_class = SintomaSerializer
