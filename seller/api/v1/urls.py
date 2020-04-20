"""
API V1: Seller Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers

from seller.api.v1.views import SellerViewSet, MySellerView, MyProductImagesViewSet

###
# Routers
###

""" Main router """
router = routers.SimpleRouter()
router.register(r'sellers', SellerViewSet, basename='sellers')
router.register(r'my-product-images', MyProductImagesViewSet, basename='my-product-images')

###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^my-seller/$', MySellerView.as_view(), name='my-seller',)
]
