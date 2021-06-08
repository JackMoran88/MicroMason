from django.urls import path
from shop_settings.views import *

from basepage.views import *

urlpatterns = [
    #
    path('connection/', TestConnection.as_view({'get': 'post'})),
    #
    path('settings/', SettingsViewSet.as_view({'get': 'list'})),
    #
    path('settings/parameters/', ParametersViewSet.as_view({'get': 'sortType'})),
    #
    path('breadcrumbs/', BreadCrumbsViewSet.as_view({'get': 'list'})),
    #
    path('settings/sliders/', SliderViewSet.as_view({'get': 'list'})),
    #

]
