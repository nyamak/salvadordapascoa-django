"""
Seller Apps
"""
###
# Libraries
###
from django.apps import AppConfig


###
# Config
###
class SellerConfig(AppConfig):
    name = 'seller'

    def ready(self):
        import seller.signals
