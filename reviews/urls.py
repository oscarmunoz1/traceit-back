from django.urls import path, include
from rest_framework import routers
from .views import ReviewsViewSet


router = routers.DefaultRouter()

router.register(r"reviews", ReviewsViewSet, basename="reviews")

urlpatterns = [
    path("", include(router.urls)),
]
