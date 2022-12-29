from django.contrib import admin

from .models import Company, Establishment


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state")
    list_filter = ("name", "city", "state")
    search_fields = ("name", "city", "state")


class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "company")
    list_filter = ("name", "city", "state", "company")
    search_fields = ("name", "city", "state", "company")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Establishment, EstablishmentAdmin)
