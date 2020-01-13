from django.contrib import admin

from .models import Item, Address, Order_Item, Order

class ItemAdmin(admin.ModelAdmin):
    list_display = ['Name','Category','Price','Discount','Details','Stock']
    list_filter = ['Category']
    list_editable = ['Category','Price','Discount','Stock']
    search_fields = ['Name']

admin.site.register(Item, ItemAdmin)

class AddressAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.User.username

    list_display = ['username', 'Apartment', "Street", 'Zip']
    list_filter = ['Street']
    list_editable = ['Apartment', 'Street', 'Zip']
    search_fields = ['username']

admin.site.register(Address, AddressAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.User.username

    def ItemDetail(self, obj):
        return obj.Item.Details

    list_display = ['username', 'Item', 'ItemDetail', 'Ordered', 'Quantity']
    list_editable = ['Ordered', 'Quantity']
    search_fields = ['username']
    ordering = ['Ordered']

admin.site.register(Order_Item, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.User.username

    list_display = ['username', 'OrderDate', 'Address', 'Payment', 'Delivered']
    list_editable = ['Payment', 'Delivered']
    search_fields = ['username', 'OrderDate', 'Address', 'Delivered']
    ordering = ['Delivered']
    filter_horizontal = ['Items']

admin.site.register(Order, OrderAdmin)

