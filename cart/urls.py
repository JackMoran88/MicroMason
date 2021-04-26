from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('cart/add/', CartViewSet.as_view({'post': 'create'})),
    path('cart/delete/', CartViewSet.as_view({'post': 'delete'})),
    path('cart/detail/', CartViewSet.as_view({'get': 'list'})),
]
