"""
Comments URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include


###
# URL Patterns
###
urlpatterns = [
    url(r'^api/v1/', include('comments.api.v1.urls'))
]
