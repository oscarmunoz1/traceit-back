from django.urls import path, include
from rest_framework import routers
from .views import ParcelViewSet, ProductsViewSet


router = routers.DefaultRouter()

router.register(r"parcels", ParcelViewSet, basename="parcels")
router.register(r"products", ProductsViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
