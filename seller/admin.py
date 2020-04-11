"""
Seller admin
"""
###
# Libraries
###

from django.contrib import admin

from seller.models import Seller, OrderMean, DeliveryMean, ProductImage


###
# Inline Admin Models
###

class InlineProductImageAdmin(admin.TabularInline):
    model = ProductImage


###
# Main Admin Models
###


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'neighborhood', 'city', 'state', 'is_approved')
    list_filter = ('city', 'state', 'delivery_means', 'order_means', 'referrals', 'is_approved')
    filter_horizontal = ('order_means', 'delivery_means',)
    inlines = [InlineProductImageAdmin,]


@admin.register(OrderMean)
class OrderMeanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


@admin.register(DeliveryMean)
class DeliveryMeanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
