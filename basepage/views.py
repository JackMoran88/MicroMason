from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *





class CategoriesListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

