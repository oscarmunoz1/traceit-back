from django.contrib import admin

from .models import Event, History


class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    ordering = ("index",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    list_filter = ("name", "date", "description")
    search_fields = ("name", "date", "description")


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name", "date", "description")
    search_fields = ("name", "date", "description")
    inlines = [
        EventInline,
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(History, HistoryAdmin)
