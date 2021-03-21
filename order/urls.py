from django.urls import path
from . import views

from order.views import *

# MEDIA
from django.conf.urls.static import static

urlpatterns = [
                  #
                  path('order/add/', OrderViewSet.as_view({'post': 'create'})),
                  path('order/list/', OrderViewSet.as_view({'post': 'list'})),
                  path('order/pay/', OrderViewSet.as_view({'post': 'pay'})),
                  #
                  path('address/add/', AddressViewSet.as_view({'post': 'create'})),
                  path('address/detail/', AddressViewSet.as_view({'post': 'list'})),
                  path('address/delete/', AddressViewSet.as_view({'post': 'delete'})),
                  #
                  # path('shipping/add/', ShippingViewSet.as_view({'post': 'create'})),
                  path('shipping/list/', ShippingViewSet.as_view({'post': 'list'})),
                  # path('shipping/delete/', ShippingViewSet.as_view({'post': 'delete'})),
                  #
                  path('payment/list/', PaymentViewSet.as_view({'post': 'list'})),
                  #
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
