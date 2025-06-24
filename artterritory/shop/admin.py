from django.contrib import admin
from .models import Category, Manufacturer, Product, Trash, TrashElement

# Register your models here.

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Trash)
admin.site.register(TrashElement)
