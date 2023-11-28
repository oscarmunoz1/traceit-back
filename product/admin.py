from django.contrib import admin

# from common.admin import GalleryImageInline
from .models import Product, Parcel
from common.models import GalleryImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


class ParcelAdmin(admin.ModelAdmin):
    list_display = ("name", "establishment")
    search_fields = ("name", "description", "establishment")


admin.site.register(Product, ProductAdmin)
admin.site.register(Parcel, ParcelAdmin)
