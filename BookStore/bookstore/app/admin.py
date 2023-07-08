from django.contrib import admin
from . models import Book

# Register your models here.

@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['ISBN', 'category', 'title', 'featured', 'topSeller', 'buying_price', 'selling_price']