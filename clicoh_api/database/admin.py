from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'stock')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'cuantity', 'product')

admin.site.register(User,UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)
