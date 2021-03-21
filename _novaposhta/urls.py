from django.urls import path
from _novaposhta.views import *

urlpatterns = [
    # http://localhost:8000/ru/api/v2/shipping/novaposhta/cities/update/
    path('cities/update/', CitiesViewSet.as_view({'get': 'update'})),
    # http://localhost:8000/ru/api/v2/shipping/novaposhta/warehouses/update/
    path('warehouses/update/', WarehouseViewSet.as_view({'get': 'update'})),
    #
]
