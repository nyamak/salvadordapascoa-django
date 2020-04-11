"""
API V1: Seller Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers

from seller.api.v1.views import SellerViewSet, MySellerView

###
# Routers
###

""" Main router """
router = routers.SimpleRouter()
router.register(r'sellers', SellerViewSet, basename='sellers')

###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^my-seller/$', MySellerView.as_view(), name='my-seller',)
]
