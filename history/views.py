from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import History, CommonEvent, WeatherEvent
from .serializers import (
    HistorySerializer,
    WeatherEventSerializer,
)
from product.models import Parcel

from datetime import datetime


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]


class EventViewSet(viewsets.ModelViewSet):
    queryset = WeatherEvent.objects.all()
    serializer_class = WeatherEventSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]

    def perform_create(self, serializer):
        parcel_id = self.request.data.get("parcel", None)
        if parcel_id is None:
            raise Exception("Parcel is required")
        parcel = Parcel.objects.get(id=parcel_id)
        if parcel.current_history is None:
            history = History.objects.create(
                name="Default History",
                description="Default History",
                start_date=datetime.now(),
                published=False,
                parcel=parcel,
            )
            parcel.current_history = history
            parcel.save()
        else:
            history = parcel.current_history
        serializer.save(history=history)
