from django.contrib import admin

from .models import (
    History,
    ChemicalEvent,
    WeatherEvent,
    GeneralEvent,
    HistoryScan,
    ProductionEvent,
)


class ChemicalEventInline(admin.TabularInline):
    model = ChemicalEvent
    extra = 1
    ordering = ("index",)


class WeatherEventInline(admin.TabularInline):
    model = WeatherEvent
    extra = 1
    ordering = ("index",)


class GeneralEventInline(admin.TabularInline):
    model = GeneralEvent
    extra = 1
    ordering = ("index",)


class ProductionEventInline(admin.TabularInline):
    model = ProductionEvent
    extra = 1
    ordering = ("index",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("date",)
    list_filter = ("date", "description")
    search_fields = ("date", "description")


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("start_date",)
    list_filter = (
        "name",
        "start_date",
    )
    search_fields = (
        "name",
        "start_date",
    )
    inlines = [
        ChemicalEventInline,
        WeatherEventInline,
        GeneralEventInline,
        ProductionEventInline,
    ]


class HistoryScanAdmin(admin.ModelAdmin):
    list_display = ("history", "ip_address", "city", "country", "date")
    list_filter = ("history", "ip_address", "city", "country", "date")


admin.site.register(WeatherEvent, EventAdmin)
admin.site.register(ChemicalEvent, EventAdmin)
admin.site.register(GeneralEvent, EventAdmin)
admin.site.register(ProductionEvent, EventAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(HistoryScan, HistoryScanAdmin)
