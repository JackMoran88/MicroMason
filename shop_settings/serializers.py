from rest_framework import serializers
from .models import *



class FooterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ('name', 'description')

class SettingDetailSerializer(serializers.ModelSerializer):
    footer = FooterDetailSerializer(many=True)
    class Meta:
        model = Setting
        fields = ('__all__')


