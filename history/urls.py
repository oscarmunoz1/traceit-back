from django.urls import path, include
from rest_framework import routers
from .views import (
    HistoryViewSet,
    EventViewSet,
    HistoryScanViewSet,
    PublicHistoryScanViewSet,
)


router = routers.DefaultRouter()

router.register(r"histories", HistoryViewSet, basename="histories")
router.register(r"events", EventViewSet, basename="events")
router.register(r"scans", HistoryScanViewSet, basename="scans")
router.register(r"public_scans", PublicHistoryScanViewSet, basename="public-scans")

urlpatterns = [
    path("", include(router.urls)),
]
