from django.contrib import admin
from .models import Gallery, GalleryImage


class GalleryImage(admin.TabularInline):
    model = GalleryImage
    extra = 1


class GalleryAdmin(admin.ModelAdmin):
    model = Gallery
    inlines = [GalleryImage]


admin.site.register(Gallery, GalleryAdmin)
