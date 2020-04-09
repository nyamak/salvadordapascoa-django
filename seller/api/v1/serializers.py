"""
API V1: Seller Serializers
"""
###
# Libraries
###

from rest_framework import serializers

from seller.models import Seller, ProductImage


###
# Serializers
###

# Product Image Serializer

class NestedProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('order', 'image',)


# Seller Serializers

class ListSellersSerializer(serializers.ModelSerializer):
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
