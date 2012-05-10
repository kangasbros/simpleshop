from django.contrib import admin
from django.utils import timezone
from simpleshop.models import Order, Product, OrderProduct

admin.site.disable_action('delete_selected')

class ModelAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    
    save_on_top = True
    
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    
    can_delete = False
    readonly_fields = ('product', 'count')
    
    def has_add_permission(self, request):
        return False

class OrderAdmin(ModelAdmin):
    actions = ('mark_paid', 'mark_shipped', 'mark_closed', 'mark_open')
    
    search_fields = ('name', 'email', 'bitcoin_address__address')
    
    list_display = ('__unicode__', 'created_at', 'total_price', 'bitcoin_payment', 'was_paid', 'was_shipped', 'closed')
    list_filter = ('created_at', 'closed')
    date_hierarchy = 'created_at'
    
    # TODO: Show paid, shipped as checkbox
    readonly_fields = ('total_price', 'bitcoin_payment', 'bitcoin_address')
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
    def mark_closed(self, request, queryset):
        queryset.filter(closed=False).update(closed=True)
    mark_closed.short_description = "Close selected orders"
    def mark_open(self, request, queryset):
        queryset.filter(closed=True).update(close=False)
    mark_open.short_description = "Re-open selected orders"
    
    def has_add_permission(self, request):
        return False
    
    # TODO: Delete order properly
    
    # TODO: Send email if shipped or paid

class ProductAdmin(ModelAdmin):
    actions = ['delete_selected']
    
    list_display = ('__unicode__', 'price', 'stock')
    list_editable = ('price', 'stock')

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
