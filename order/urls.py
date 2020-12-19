from django.urls import path
from . import views

from order.views import *

urlpatterns = [
    path('order/add/', OrderViewSet.as_view({'post': 'create'})),
    path('order/delete/', OrderViewSet.as_view({'post': 'delete'})),
    path('order/detail/', OrderViewSet.as_view({'post': 'list'})),
]
