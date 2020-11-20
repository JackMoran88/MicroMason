from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets

from .serializers import *
from .models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q

from channels.layers import get_channel_layer




class SettingsViewSet(viewsets.ViewSet):

    def list(self, request):
        settings = Setting.objects.all()
        serializer = SettingDetailSerializer(settings, many=True)
        return Response(serializer.data)