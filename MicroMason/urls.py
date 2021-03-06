"""MicroMason URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# MEDIA
from django.conf.urls.static import static
from django.conf import settings

# from basepage.views import AuthCheck

from basepage.views import *
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = 'MicroMason'  # default: "Django Administration"
admin.site.index_title = 'Администрирование MicroMason'  # default: "Site administration"
admin.site.site_title = 'Администрирование MicroMason'  # default: "Django site admin"

urlpatterns = [
                  path('api/admin/', admin.site.urls),
                  path('api/api-auth/', include('rest_framework.urls')),
                  #
                  path('api/ckeditor/', include('ckeditor_uploader.urls')),
                  #
                  path('api/v2/auth/', include('djoser.urls')),
                  path('api/v2/auth/', include('djoser.urls.authtoken')),
                  path('api/v2/auth/', include('djoser.urls.jwt')),
                  #
                  path('api/v2/', include('basepage.urls')),
                  path('api/v2/', include('shop_settings.urls')),
                  path('api/v2/', include('product.urls')),
                  path('api/v2/', include('cart.urls')),
                  path('api/v2/', include('order.urls')),
                  # path('api/v2/', include('user.urls')),
                  #

                  path('user/password/reset/confirm/<str:uid>/<str:token>',
                       RedirectToFront.as_view({'get': 'pass_reset_confirm'})),
                  #
                  # path('api/v2/novaposhta/', include('novaposhta.urls')),
                  path('api/v2/novaposhta/search/', NovaPoshtaViewSet.as_view({'post': 'search'})),

                  path('i18n/', include('django.conf.urls.i18n')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('api/v2/shipping/novaposhta/', include('_novaposhta.urls'))
)
