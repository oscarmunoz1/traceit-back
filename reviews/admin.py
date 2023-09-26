from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "production")
    search_fields = ("user",)


admin.site.register(Review, ReviewAdmin)
