from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from .models import (
    History,
    ProductionEvent,
    WeatherEvent,
    ChemicalEvent,
    GeneralEvent,
    HistoryScan,
)
from .serializers import (
    HistorySerializer,
    WeatherEventSerializer,
    ProductionEventSerializer,
    ChemicalEventSerializer,
    GeneralEventSerializer,
    PublicHistorySerializer,
    ListHistoryClassSerializer,
    UpdateChemicalEventSerializer,
    UpdateWeatherEventSerializer,
    UpdateProductionEventSerializer,
    UpdateGeneralEventSerializer,
)
from .constants import (
    WEATHER_EVENT_TYPE,
    PRODUCTION_EVENT_TYPE,
    CHEMICAL_EVENT_TYPE,
    event_map,
    ALLOWED_PERIODS,
)

from product.models import Parcel, Product
from backend.permissions import CompanyNestedViewSet


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        if self.action == "public_history":
            return History.objects.filter(published=True)
        else:
            return History.objects.all()

    def create(self, request):
        data = request.data
        parcel = Parcel.objects.get(id=data["parcel"])
        product = data["product"]
        obj, created = Product.objects.get_or_create(name=product["name"])
        type = data["type"]
        age_of_plants = data["age_of_plants"]
        number_of_plants = data["number_of_plants"]
        soil_ph = data["soil_ph"]
        is_outdoor = data["is_outdoor"]
        extra_data = {
            "age_of_plants": age_of_plants,
            "number_of_plants": number_of_plants,
            "soil_ph": soil_ph,
            "is_outdoor": is_outdoor,
        }
        history = History.objects.create(
            start_date=data["date"],
            parcel=parcel,
            product=obj,
            extra_data=extra_data,
            type=type,
        )
        parcel.current_history = history
        parcel.save()
        serializer = HistorySerializer(history)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    @permission_classes([AllowAny])
    def public_history(self, request, pk=None):
        queryset = self.get_queryset()

        history = get_object_or_404(queryset, pk=pk)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("HTTP_X_REAL_IP")

        city = None
        country = None

        if ip_address:
            try:
                g = GeoIP2()
                city = g.city(ip_address).get("city")
                country = g.country(ip_address).get("country_name")
            except Exception as e:
                pass

        history_scan = HistoryScan.objects.create(
            history=history,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip_address,
            city=city,
            country=country,
        )
        serializer = PublicHistorySerializer(
            history, context={"history_scan": history_scan.id}
        )
        return Response(serializer.data)


class PublicHistoryScanViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=["post"])
    @permission_classes([AllowAny])
    def comment(self, request, pk=None):
        history_scan = get_object_or_404(HistoryScan, pk=pk)
        comment = request.data.get("comment", None)
        if comment is None:
            return Response(
                {"error": "Comment is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        history_scan.comment = comment
        history_scan.save()
        return Response(status=status.HTTP_200_OK)


class HistoryScanViewSet(CompanyNestedViewSet, viewsets.ModelViewSet):
    queryset = HistoryScan.objects.all()
    serializer_class = ListHistoryClassSerializer

    @action(detail=False, methods=["get"])
    def list_scans_by_establishment(
        self, request, parcel_pk=None, company_pk=None, establishment_pk=None
    ):
        parcel = request.query_params.get("parcel", None)
        product = request.query_params.get("product", None)
        period = request.query_params.get("period", None)
        production = request.query_params.get("production", None)
        if period is None or period not in ALLOWED_PERIODS:
            return Response(
                {"error": "Period is required and must be week, month or year"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.establishment is None:
            return Response(
                {"error": "Establishment is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get date kwargs for filter by period
        date_kwargs = {}
        if period == "week":
            date_kwargs["date__gte"] = datetime.now() - timedelta(days=7)
        elif period == "month":
            date_kwargs["date__gte"] = datetime.now() - timedelta(days=30)
        elif period == "year":
            date_kwargs["date__gte"] = datetime.now() - timedelta(days=365)

        # Get last 9 scans from the establishment
        history_scans = HistoryScan.objects.filter(
            history__parcel__establishment=self.establishment,
            **date_kwargs,
        ).order_by("-date")
        if parcel is not None:
            history_scans = history_scans.filter(history__parcel__id=parcel)
        if product is not None:
            history_scans = history_scans.filter(history__product__id=product)
        if production is not None:
            history_scans = history_scans.filter(history__id=production)
        return Response(
            ListHistoryClassSerializer(
                history_scans[0:9], many=True, context={"history_scan": True}
            ).data
        )


class EventViewSet(CompanyNestedViewSet, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        event_type = (
            self.request.data.get("event_type")
            if "event_type" in self.request.data
            else self.request.query_params.get("event_type", None)
        )
        if event_type is None:
            raise Exception("Event type is required")
        event_type = int(event_type)
        if event_type == WEATHER_EVENT_TYPE:
            if (
                self.action == "create"
                or self.action == "update"
                or self.action == "partial_update"
            ):
                return UpdateWeatherEventSerializer
            return WeatherEventSerializer
        elif event_type == PRODUCTION_EVENT_TYPE:
            if (
                self.action == "create"
                or self.action == "update"
                or self.action == "partial_update"
            ):
                return UpdateProductionEventSerializer
            return ProductionEventSerializer
        elif event_type == CHEMICAL_EVENT_TYPE:
            if (
                self.action == "create"
                or self.action == "update"
                or self.action == "partial_update"
            ):
                return UpdateChemicalEventSerializer
            return ChemicalEventSerializer
        else:
            if (
                self.action == "create"
                or self.action == "update"
                or self.action == "partial_update"
            ):
                return UpdateGeneralEventSerializer
            return GeneralEventSerializer

    def get_queryset(self):
        event_type = (
            self.request.data.get("event_type")
            if "event_type" in self.request.data
            else self.request.query_params.get("event_type", None)
        )
        if event_type == WEATHER_EVENT_TYPE:
            return WeatherEvent.objects.all()
        elif event_type == PRODUCTION_EVENT_TYPE:
            return ProductionEvent.objects.all()
        elif event_type == CHEMICAL_EVENT_TYPE:
            return ChemicalEvent.objects.all()
        else:
            return GeneralEvent.objects.all()

    def perform_create(self, serializer):
        parcels = self.request.data.get("parcels", None)
        event_type = int(self.request.data.get("event_type", None))
        if parcels is None or parcels is []:
            raise Exception("Parcel is required")
        parcels = Parcel.objects.filter(id__in=parcels).select_related(
            "current_history"
        )
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
            event_model = event_map.get(event_type, GeneralEvent)
            index = (
                history.history_weatherevent_events.count()
                + history.history_chemicalevent_events.count()
                + history.history_generalevent_events.count()
                + history.history_productionevent_events.count()
            ) + 1
            event_model.objects.create(
                history=history, index=index, **serializer.validated_data
            )
        serializer.save()
