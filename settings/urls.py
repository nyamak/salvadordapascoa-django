"""
SalvadorDaPascoa URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include
from django.contrib import admin

from helpers.health_check_view import health_check

###
# URLs
###
urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Health Check
    url(r'health-check/$', health_check, name='health_check'),

    # Applications
    url(r'^', include('accounts.urls')),
    url(r'^', include('seller.urls')),
    url(r'^', include('comments.urls')),
]


admin.site.site_header = "Salvador da Páscoa - Admin"
admin.site.site_title = "Portal de Administrador - Salvador da Páscoa"
admin.site.index_title = "Painel de administração"