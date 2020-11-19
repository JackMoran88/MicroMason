from django.urls import path
from . import views

from basepage.views import *

urlpatterns = [
    #
    path('categories/', CategoryViewSet.as_view({'post': 'list'})),
    path('category/<slug>/', CategoryViewSet.as_view({'post': 'retrieve'})),
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
    path('product/', ProductViewSet.as_view({'post': 'retrieve'})),
    #
    path('auth/check/', CustomerViewSet.as_view({'post': 'check'})),
    path('customer/set_username/', CustomerViewSet.as_view({'post': 'setFullName'})),
    path('customer/detail/', CustomerViewSet.as_view({'post': 'retrieve'})),
    #
    path('anonymous/', AnonymousViewSer.as_view({'post': 'create'})),
    #

]
