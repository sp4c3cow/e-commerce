from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'availability', 'created', 'updated']
    list_filter = ['availability', 'created', 'updated']
    list_editable = ['price', 'availability']
    prepopulated_fields = {'slug': ('name',)}
