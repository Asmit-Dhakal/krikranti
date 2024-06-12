from django.contrib import admin
from .models import Product, Category, Sub_category, order, OrderUpdate

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(order)
admin.site.register(OrderUpdate)