from django.contrib import admin
from django.utils import timezone
from simpleshop.models import Order, Product, OrderProduct

class ModelAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    
    save_on_top = True
    
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(ModelAdmin):
    actions = ('mark_paid', 'mark_shipped')
    
    search_fields = ('name', 'email', 'bitcoin_address__address')
    
    list_display = ('__unicode__', 'created_at', 'total_price', 'bitcoin_payment', 'was_paid', 'was_shipped')
    date_hierarchy = 'created_at'
    
    # TODO: Show price, Bitcoin price, and items as static
    # TODO: Show paid, shipped as checkbox
    fieldsets = [
        ('Buyer Information', {'fields': ['name', 'email']}),
        ('Payment Information', {'fields': ['total_price', 'bitcoin_payment', 'bitcoin_address', 'paid_at']}),
        ('Shipping Information', {'fields': ['address', 'shipped_at']})
    ]
    inlines = [OrderProductInline]
    
    def mark_paid(self, request, queryset):
        queryset.filter(paid_at=None).update(paid_at=timezone.now())
    mark_paid.short_description = "Mark selected orders as paid for"
    def mark_shipped(self, request, queryset):
        queryset.filter(shipped_at=None).update(shipped_at=timezone.now())
    mark_shipped.short_description = "Mark selected orders as shipped"
    
    # TODO: Delete order properly
    
    # TODO: Send email if shipped or paid

class ProductAdmin(ModelAdmin):
    list_display = ('__unicode__', 'price', 'stock')
    list_editable = ('price', 'stock')

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
