from rest_framework.serializers import ModelSerializer

from .models import *


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
