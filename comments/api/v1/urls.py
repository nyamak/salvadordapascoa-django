"""
API V1: Comments Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers


###
# Routers
###
""" Main router """
router = routers.SimpleRouter()


###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
]
