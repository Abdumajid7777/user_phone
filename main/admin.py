from django.contrib import admin
from .models import Phone,PhoneReview, Phone_Parts, Brand, Color, Accessory, Cart, CartItem, Order, OrderItem

admin.site.register(Phone)
admin.site.register(PhoneReview)
admin.site.register(Phone_Parts)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Accessory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)