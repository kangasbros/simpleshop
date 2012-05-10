from django.contrib import admin
from django.utils import timezone
from simpleshop.models import Order, Product, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    actions = ['mark_shipped']
    
    # TODO: Add option to mark paid or shipped
    list_display = ['__unicode__', 'created_at', 'price_total', 'bitcoin_payment', 'was_paid', 'was_shipped']
    list_filter = ['created_at']
    
    # TODO: Show price, Bitcoin price, and items as static
    # TODO: Show paid, shipped as checkbox
    fieldsets = [
        ('Buyer Information', {'fields': ['name', 'email']}),
        ('Payment Information', {'fields': ['price_total', 'bitcoin_payment', 'bitcoin_address', 'paid_at']}),
        ('Shipping Information', {'fields': ['address', 'shipped_at']})
    ]
    inlines = [OrderProductInline]
    
    def mark_shipped(self, request, queryset):
        queryset.update(shipped_at=timezone.now())
    mark_shipped.short_description = "Mark selected orders as shipped"
    # TODO: Send email if shipped or paid

admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
