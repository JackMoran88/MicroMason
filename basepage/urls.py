from django.urls import path
from . import views

from basepage.views import *

urlpatterns = [
    #
    path('categories/', CategoryViewSet.as_view({'post': 'list'})),
    path('category/detail/', CategoryViewSet.as_view({'post': 'details'})),
    path('category/detail/sort/', CategoryViewSet.as_view({'post': 'details'})),
    path('category/search/list/', CategoryViewSet.as_view({'post': 'search_list'})),
    #
    path('cart/add/', CartViewSet.as_view({'post': 'create'})),
    path('cart/delete/', CartViewSet.as_view({'post': 'delete'})),
    path('cart/detail/', CartViewSet.as_view({'post': 'list'})),
    #
    path('wish/add/', WishViewSet.as_view({'post': 'create'})),
    path('wish/delete/', WishViewSet.as_view({'post': 'delete'})),
    path('wish/detail/', WishViewSet.as_view({'post': 'list'})),
    #
    path('review/add/', ReviewViewSet.as_view({'post': 'create'})),
    path('review/delete/', ReviewViewSet.as_view({'post': 'delete'})),
    path('review/detail/', ReviewViewSet.as_view({'post': 'list'})),
    path('review/answer/', ReviewViewSet.as_view({'post': 'answer'})),
    #
    path('products/', ProductViewSet.as_view({'post': 'list'})),
    path('products/search/detail/', ProductViewSet.as_view({'post': 'search_detail'})),
    path('products/search/list/', ProductViewSet.as_view({'post': 'search_list'})),
    path('product/', ProductViewSet.as_view({'post': 'retrieve'})),
    #
    path('auth/check/', CustomerViewSet.as_view({'post': 'check'})),
    path('customer/change/', CustomerViewSet.as_view({'post': 'change'})),
    path('customer/detail/', CustomerViewSet.as_view({'post': 'retrieve'})),
    #
    path('anonymous/', AnonymousViewSer.as_view({'post': 'create'})),
    #
    path('test/', ProductPaginationGeneric.as_view({'post': 'list'})),
    #


]
