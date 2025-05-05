from django.contrib import admin
from .models import Category, Address, Business
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'city']
    
@admin.register(Business)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


