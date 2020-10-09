from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data






class CategoryListSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'children')