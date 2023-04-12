from django.urls import path, include
from rest_framework import routers
from .views import ParcelViewSet


router = routers.DefaultRouter()

router.register(r"parcels", ParcelViewSet, basename="parcels")

urlpatterns = [
    path("", include(router.urls)),
]
