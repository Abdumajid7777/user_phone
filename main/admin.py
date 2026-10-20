from django.contrib import admin
from .models import Notification, Review, Accessory, Brand, Color, Phone, Cart, CartItem, Order, OrderItem, Favorite

admin.site.register(Phone)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Accessory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Notification)
admin.site.register(Review)
admin.site.register(Favorite)

