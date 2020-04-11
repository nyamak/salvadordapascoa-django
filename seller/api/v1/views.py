"""
API V1: Seller Views
"""
###
# Libraries
###

import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, permissions
from rest_framework.generics import GenericAPIView

from helpers.pagination import CustomResultsSetPagination
from seller.api.v1.serializers import ListSellersSerializer, SellerDetailsSerializer, SellerCreationSerializer
from seller.models import Seller

###
# Filters
###


class SellerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='name_search')
    city = django_filters.CharFilter(method='city_search')
    state = django_filters.CharFilter(method='state_search')
    neighborhood = django_filters.CharFilter(method='neighborhood_search')

    class Meta:
        model = Seller
        fields = ('city', 'state', 'name')

    def name_search(self, queryset, name, value):
        for word in value.split(' '):
            queryset = queryset.filter(
                Q(instagram_profile__icontains=word) |
                Q(name__icontains=word)
            )
        return queryset

    def city_search(self, queryset, city, value):
        for word in value.split(' '):
            queryset = queryset.filter(city__icontains=word)
        return queryset

    def state_search(self, queryset, state, value):
        for word in value.split(' '):
            queryset = queryset.filter(state__icontains=word)
        return queryset

    def neighborhood_search(self, queryset, neighborhood, value):
        for word in value.split(' '):
            queryset = queryset.filter(neighborhood__icontains=word)
        return queryset


###
# Viewsets
###


class SellerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = CustomResultsSetPagination
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SellerFilter
    queryset = Seller.objects.all()
    lookup_field = 'instagram_profile'
    lookup_url_regex = r'@(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}'
    serializer_classes = {
        'list': ListSellersSerializer,
        'retrieve': SellerDetailsSerializer,
    }

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_approved=True)
        return queryset.prefetch_related('order_means', 'delivery_means', 'product_images')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action) or ListSellersSerializer


class MySellerView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = SellerCreationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.seller

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
