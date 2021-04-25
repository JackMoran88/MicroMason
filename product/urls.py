from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('products/', ProductViewSet.as_view({'post': 'list'})),
    path('products/search/detail/', ProductViewSet.as_view({'get': 'search_detail'})),
    path('products/search/list/', ProductViewSet.as_view({'post': 'search_list'})),
    path('products/last/', ProductViewSet.as_view({'get': 'last_added'})),
    path('products/popular/', ProductViewSet.as_view({'get': 'most_popular'})),
    path('products/querysets/', ProductViewSet.as_view({'get': 'querysets'})),
    path('product/', ProductViewSet.as_view({'post': 'retrieve'})),



    path('test/', ProductPaginationGeneric.as_view({'post': 'list'})),

]
