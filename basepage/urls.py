from django.urls import path
from . import views

from basepage.views import *

urlpatterns = [
    #
    path('categories/', CategoryViewSet.as_view({'post': 'list'})),
    path('category/products/', CategoryViewSet.as_view({'post': 'detail_products'})),
    path('category/detail/', CategoryViewSet.as_view({'post': 'retrieve'})),
    # path('category/detail/sort/', CategoryViewSet.as_view({'post': 'detail_products'})),
    path('category/search/list/', CategoryViewSet.as_view({'post': 'search_list'})),
    #
    path('wish/add/', WishViewSet.as_view({'post': 'create'})),
    path('wish/delete/', WishViewSet.as_view({'post': 'delete'})),
    path('wish/detail/', WishViewSet.as_view({'post': 'list'})),
    #
    path('compare/add/', CompareViewSet.as_view({'post': 'create'})),
    path('compare/delete/', CompareViewSet.as_view({'post': 'delete'})),
    path('compare/list/', CompareViewSet.as_view({'post': 'list'})),
    #
    path('review/add/', ReviewViewSet.as_view({'post': 'create'})),
    path('review/delete/', ReviewViewSet.as_view({'post': 'delete'})),
    path('review/detail/', ReviewViewSet.as_view({'post': 'list'})),
    path('review/answer/', ReviewViewSet.as_view({'post': 'answer'})),
    path('review/customer/', ReviewViewSet.as_view({'post': 'user_list'})),
    #
    path('auth/check/', CustomerViewSet.as_view({'post': 'check'})),
    path('customer/change/', CustomerViewSet.as_view({'post': 'change'})),
    path('customer/detail/', CustomerViewSet.as_view({'post': 'retrieve'})),
    #
    path('anonymous/', AnonymousViewSet.as_view({'post': 'create'})),
    #

]
