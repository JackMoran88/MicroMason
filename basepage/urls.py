from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),



    path('api/sign_up/', views.api_sign_up),
    path('api/sign_in/', views.api_sign_in)
]
