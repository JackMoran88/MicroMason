from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import permissions

from .serializers import *
from .models import *





class CategoriesListView(APIView):
    # permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all().filter(parent__isnull=True)
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

