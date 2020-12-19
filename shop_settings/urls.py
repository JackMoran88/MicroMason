from django.urls import path
from shop_settings.views import *

from basepage.views import *

urlpatterns = [
    #
    path('connection/', TestConnection.as_view({'post': 'post'})),
    #
    path('settings/', SettingsViewSet.as_view({'post': 'list'})),
    #
    path('settings/parameters/', ParametersViewSet.as_view({'post': 'sortType'})),
    #
    path('breadcrumbs/', BreadCrumbsViewSet.as_view({'post': 'list'})),
    #
    path('settings/sliders/', SliderViewSet.as_view({'post': 'list'})),
    #

]
