from django.urls import path
from . import views

from basepage.views import *

urlpatterns = [
    path('categories/', views.CategoriesListView.as_view()),
    path('category/<slug>/', CategoryDetailView.as_view()),

    path('product/<slug>/', ProductDetailView.as_view()),

    path('review/', ReviewCreateView.as_view()),
    path('rating/', AddRatingView.as_view()),

]
