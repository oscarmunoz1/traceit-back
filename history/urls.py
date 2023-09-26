from django.urls import path, include
from rest_framework import routers
from .views import HistoryViewSet, EventViewSet, HistoryScanViewSet


router = routers.DefaultRouter()

router.register(r"histories", HistoryViewSet, basename="histories")
router.register(r"events", EventViewSet, basename="events")
router.register(r"scans", HistoryScanViewSet, basename="scans")

urlpatterns = [
    path("", include(router.urls)),
]
