"""
API V1: Seller Serializers
"""
###
# Libraries
###

from rest_framework import serializers

from seller.models import Seller, ProductImage, DeliveryMean, OrderMean


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


class SellerCreationSerializer(serializers.ModelSerializer):
    delivery_means = serializers.SlugRelatedField(queryset=DeliveryMean.objects.all(), slug_field='slug', many=True)
    order_means = serializers.SlugRelatedField(queryset=OrderMean.objects.all(), slug_field='slug', many=True)
    product_images = NestedProductImageSerializer(many=True)

    def create(self, validated_data):
        product_images_data = validated_data.pop('product_images')
        seller = Seller.objects.create(**validated_data)
        for product_image in product_images_data:
            ProductImage.objects.create(seller=seller, **product_image)
        return seller

    class Meta:
        model = Seller
        fields = (
            'user', 'name', 'description', 'neighborhood', 'city', 'state', 'delivery_means', 'order_means',
            'telephone_number', 'whatsapp_number', 'instagram_profile', 'ifood_url', 'uber_eats_url', 'rappi_url',
            'site_url', 'cover_image', 'product_images', 'referrals', 'is_approved',
        )
        read_only_fields = ('id', 'user', 'is_approved',)

