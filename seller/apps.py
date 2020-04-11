"""
Seller Apps
"""
###
# Libraries
###
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

###
# Config
###
class SellerConfig(AppConfig):
    name = 'seller'
    verbose_name = _('Vendedores')

    def ready(self):
        import seller.signals
