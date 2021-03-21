from django.urls import path, include
from . import views

from basepage.views import *

urlpatterns = [
    #
    path('categories/', CategoryViewSet.as_view({'post': 'list'})),
    path('category/products/', CategoryViewSet.as_view({'post': 'detail_products'})),
    path('category/detail/', CategoryViewSet.as_view({'post': 'retrieve'})),
    # path('category/detail/sort/', CategoryViewSet.as_view({'post': 'detail_products'})),
    path('category/search/list/', CategoryViewSet.as_view({'post': 'search_list'})),
    #
    path('wish/add/', WishViewSet.as_view({'post': 'create'})),
    path('wish/delete/', WishViewSet.as_view({'post': 'delete'})),
    path('wish/detail/', WishViewSet.as_view({'post': 'list'})),
    #
    path('compare/add/', CompareViewSet.as_view({'post': 'create'})),
    path('compare/delete/', CompareViewSet.as_view({'post': 'delete'})),
    path('compare/list/', CompareViewSet.as_view({'post': 'list'})),
    #
    path('review/add/', ReviewViewSet.as_view({'post': 'create'})),
    path('review/delete/', ReviewViewSet.as_view({'post': 'delete'})),
    path('review/detail/', ReviewViewSet.as_view({'post': 'list'})),
    path('review/answer/', ReviewViewSet.as_view({'post': 'answer'})),
    path('review/customer/', ReviewViewSet.as_view({'post': 'user_list'})),
    #
    path('auth/check/', CustomerViewSet.as_view({'post': 'check'})),
    path('customer/change/', CustomerViewSet.as_view({'post': 'change'})),
    path('customer/detail/', CustomerViewSet.as_view({'post': 'retrieve'})),

    path('auth/social/token/', CustomerSocial.as_view({'post': 'social'})),
    path('auth/social/', include('rest_framework_social_oauth2.urls')),

    #
    path('anonymous/', AnonymousViewSet.as_view({'post': 'create'})),
    #

]

# {"web": {"client_id": "1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com",
#          "project_id": "micromason", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#          "token_uri": "https://oauth2.googleapis.com/token",
#          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#          "client_secret": "IWH3HU3Lpvcp25_PHXeuhL6q"}}

# https://accounts.google.com/o/oauth2/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost:8080&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&client_id=1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com

#
# https://accounts.google.com/o/oauth2/v2/auth?
#  scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&
#  access_type=offline&
#  include_granted_scopes=true&
#  response_type=code&
#  state=state_parameter_passthrough_value&
#  redirect_uri=http%3A//localhost:8080&
#  client_id=1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com
