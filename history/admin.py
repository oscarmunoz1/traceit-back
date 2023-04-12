from django.contrib import admin

from .models import History, ChemicalEvent, WeatherEvent, GeneralEvent


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


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    list_filter = ("name", "date", "description")
    search_fields = ("name", "date", "description")


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("start_date",)
    list_filter = ("name", "start_date", "description")
    search_fields = ("name", "start_date", "description")
    inlines = [ChemicalEventInline, WeatherEventInline, GeneralEventInline]


admin.site.register(WeatherEvent, EventAdmin)
admin.site.register(History, HistoryAdmin)
