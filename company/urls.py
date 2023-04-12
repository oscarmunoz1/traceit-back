from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet, EstablishmentViewSet


router = routers.DefaultRouter()

router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"establishments", EstablishmentViewSet, basename="establishments")

urlpatterns = [
    path("", include(router.urls)),
]
