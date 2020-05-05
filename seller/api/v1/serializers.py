"""
API V1: Seller Serializers
"""
###
# Libraries
###
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from seller.constants import MEANS_FIELDS_PAIRS
from seller.models import Seller, ProductImage, DeliveryMean, OrderMean


###
# Serializers
###

# Product Image Serializer

class NestedProductImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {
                'image': instance.image.url or instance.legacy_image,
            }
        )
        return data

    class Meta:
        model = ProductImage
        fields = ('id', 'order', 'image',)


# Seller Serializers

class ListSellersSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {
                'cover_image': instance.cover_image or instance.legacy_cover_image,
            }
        )
        return data

    class Meta:
        model = Seller
        fields = (
            'instagram_profile', 'name', 'neighborhood', 'city', 'state', 'description', 'telephone_number',
            'cover_image',
        )


class SellerDetailsSerializer(serializers.ModelSerializer):
    product_images = NestedProductImageSerializer(many=True)
    order_means = serializers.SerializerMethodField()
    delivery_means = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {
                'cover_image': instance.cover_image or instance.legacy_cover_image,
            }
        )
        return data

    def get_order_means(self, instance):
        return [mean.name for mean in instance.order_means.all()]

    def get_delivery_means(self, instance):
        return [mean.name for mean in instance.delivery_means.all()]

    class Meta:
        model = Seller
        fields = (
            'instagram_profile', 'name', 'neighborhood', 'city', 'state', 'description', 'telephone_number',
            'cover_image', 'whatsapp_number', 'delivery_means', 'order_means', 'product_images',
        )


class SellerCreationSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    delivery_means = serializers.SlugRelatedField(queryset=DeliveryMean.objects.all(), slug_field='slug', many=True)
    order_means = serializers.SlugRelatedField(queryset=OrderMean.objects.all(), slug_field='slug', many=True)
    product_images = NestedProductImageSerializer(many=True, required=False)

    def validate(self, data):
        order_means = data.get('order_means')
        for mean in order_means:
            if MEANS_FIELDS_PAIRS.get(mean.slug) not in list(data.keys()):
                raise ValidationError(_(f'{mean.name} é citado como meio de pedido, mas dados não foram fornecidos.'))

        return data

    class Meta:
        model = Seller
        fields = (
            'user', 'name', 'description', 'neighborhood', 'city', 'state', 'delivery_means', 'order_means',
            'telephone_number', 'whatsapp_number', 'instagram_profile', 'ifood_url', 'uber_eats_url', 'rappi_url',
            'site_url', 'cover_image', 'product_images', 'referrals', 'is_approved',
        )
        read_only_fields = ('id', 'user', 'is_approved', 'product_images',)

