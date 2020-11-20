from django.urls import path
from shop_settings.views import *

from basepage.views import *

urlpatterns = [
    #
    path('settings/', SettingsViewSet.as_view({'post': 'list'})),
    #

]
