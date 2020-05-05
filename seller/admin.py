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
    actions = ['approve_sellers']

    def approve_sellers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_sellers.short_description = 'Aprovar Vendedores selecionados'

@admin.register(OrderMean)
class OrderMeanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


@admin.register(DeliveryMean)
class DeliveryMeanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
