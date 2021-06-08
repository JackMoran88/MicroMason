from django.urls import path, include
from . import views

from basepage.views import *

urlpatterns = [
    #
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('category/products/', CategoryViewSet.as_view({'get': 'detail_products'})),
    path('category/detail/', CategoryViewSet.as_view({'get': 'retrieve'})),
    path('category/search/list/', CategoryViewSet.as_view({'get': 'search_list'})),
    #
    path('wish/add/', WishViewSet.as_view({'post': 'create'})),
    path('wish/delete/', WishViewSet.as_view({'post': 'delete'})),
    path('wish/detail/', WishViewSet.as_view({'get': 'list'})),
    path('wish/ids/', WishViewSet.as_view({'get': 'ids'})),
    #
    path('compare/add/', CompareViewSet.as_view({'post': 'create'})),
    path('compare/delete/', CompareViewSet.as_view({'post': 'delete'})),
    path('compare/list/', CompareViewSet.as_view({'get': 'list'})),
    #
    path('review/add/', ReviewViewSet.as_view({'post': 'create'})),
    path('review/delete/', ReviewViewSet.as_view({'post': 'delete'})),
    path('review/detail/', ReviewViewSet.as_view({'get': 'list'})),
    path('review/answer/', ReviewViewSet.as_view({'post': 'answer'})),
    path('review/customer/', ReviewViewSet.as_view({'post': 'user_list'})),
    #
    path('auth/check/', CustomerViewSet.as_view({'post': 'check'})),
    path('customer/change/', CustomerViewSet.as_view({'post': 'change'})),
    path('customer/detail/', CustomerViewSet.as_view({'get': 'retrieve'})),

    path('auth/social/token/', CustomerSocial.as_view({'post': 'social'})),
    path('auth/social/', include('rest_framework_social_oauth2.urls')),

    #
    path('anonymous/', AnonymousViewSet.as_view({'get': 'create'})),
    path('anonymous/check/', AnonymousViewSet.as_view({'post': 'check'})),
    #

]
