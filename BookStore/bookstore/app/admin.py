from django.contrib import admin
from . models import *

# Register your models here.

@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['ISBN', 'category', 'title', 'featured', 'topSeller', 'buying_price', 'selling_price']

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'firstname', 'lastname']

@admin.register(Promotion)
class PromotionModelAdmin(admin.ModelAdmin):
    list_display = ['promocode', 'percentage']