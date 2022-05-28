from django.contrib import admin
from .models import Product, Order, OrderItem, ColourVariation, SizeVariation

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColourVariation)
admin.site.register(SizeVariation)