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
        parcels = self.request.data.get("parcels", None)
        if parcels is None or parcels is []:
            raise Exception("Parcel is required")
        parcels = Parcel.objects.filter(id__in=parcels)
        for parcel in parcels:
            if parcel.current_history is None:
                history = History.objects.create(
                    name="Default History",
                    start_date=datetime.now(),
                    published=False,
                    parcel=parcel,
                )
                parcel.current_history = history
                parcel.save()
            else:
                history = parcel.current_history
            WeatherEvent.objects.create(history=history, **serializer.validated_data)
