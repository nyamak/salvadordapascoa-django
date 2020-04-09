"""
API V1: Seller Views
"""
###
# Libraries
###
from rest_framework import mixins, viewsets, permissions

from seller.api.v1.serializers import ListSellersSerializer, SellerDetailsSerializer
from seller.models import Seller

###
# Filters
###


###
# Viewsets
###

class SellerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Seller.objects.all()
    lookup_field = 'instagram_profile'
    lookup_url_regex = r'@(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}'
    serializer_classes = {
        'list': ListSellersSerializer,
        'retrieve': SellerDetailsSerializer,
    }

    def filter_queryset(self, queryset):
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_approved=True)
        return queryset.prefetch_related('order_means', 'delivery_means', 'product_images')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action) or ListSellersSerializer
