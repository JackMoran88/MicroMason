from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets

from .serializers import *
from .models import *
from basepage.models import *
from product.models import *


from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q

from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404

class TestConnection(viewsets.ViewSet):
    def post(self, request):
        return Response(status=200)


class SettingsViewSet(viewsets.ViewSet):

    def list(self, request):
        settings = Setting.objects.all()
        serializer = SettingDetailSerializer(settings, many=True)
        return Response(serializer.data)


class ParametersViewSet(viewsets.ViewSet):

    def sortType(self, request):
        settings = ProductSortType.objects.all().order_by('order')
        serializer = ProductSortTypeSerializer(settings, many=True)
        return Response(serializer.data)


class BreadCrumbsViewSet(viewsets.ViewSet):

    def list(self, request):
        crumb = request.GET.get('breadcrumb')
        CategoryQuery = Category.objects.filter(slug=crumb).first()
        if(CategoryQuery):
            serializer = BreadCrumbCategorySerializer(CategoryQuery)
            return Response(serializer.data)

        ProductQuery = Product.objects.filter(slug=crumb).first()
        if (ProductQuery):
            serializer = BreadCrumbCategorySerializer(ProductQuery)
            return Response(serializer.data)

        else:
            return Response()


class SliderViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Slider.objects.all()
        serializer = SliderDetailSerializer(queryset, many=True)
        return Response(serializer.data)


