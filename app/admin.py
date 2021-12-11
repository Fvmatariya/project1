from django.contrib import admin
from .models import *

admin.site.register(User)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','id','price','cate']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','uid','product','status']

@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['id','uid','product','amount']