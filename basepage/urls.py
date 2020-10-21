from django.urls import path
from . import views

from basepage.views import *

urlpatterns = [
    path('categories/', views.CategoriesListView.as_view()),
    path('category/<slug>/', CategoryDetailView.as_view()),

    path('product/<slug>/', ProductDetailView.as_view()),

    path('review/', ReviewCreateView.as_view()),
    path('rating/', AddRatingView.as_view()),

    path('cart/add/', AddCartView.as_view()),
    path('cart/detail/', CartDetailView.as_view()),


    path('anonymous/', AnonymousCustomerCreateView.as_view()),



    path('wish/add/', AddWishView.as_view()),
    path('wish/detail/', DetailWishView.as_view()),
    # path('wish/detail/id/', DetailIDWishView.as_view()),
    path('wish/delete/', DeleteWishView.as_view()),




    path('customer/detail/', DetailCustomerView.as_view()),

]
