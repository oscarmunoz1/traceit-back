from rest_framework import serializers

from .models import (
    History,
    CommonEvent,
    ChemicalEvent,
    WeatherEvent,
    GeneralEvent,
    HistoryScan,
    ProductionEvent,
)
from .constants import (
    WEATHER_EVENT_TYPE,
    PRODUCTION_EVENT_TYPE,
    CHEMICAL_EVENT_TYPE,
    GENERAL_EVENT_TYPE,
)
from common.models import Gallery
from product.models import Product, Parcel
from company.models import Establishment


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CommonEvent
        fields = "__all__"

    def get_image(self, event):
        if event.album is not None:
            return event.album.images.first().image.url
        return None


class UpdateChemicalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalEvent
        fields = "__all__"


class ChemicalEventSerializer(EventSerializer):
    type = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField()

    class Meta:
        model = ChemicalEvent
        fields = "__all__"

    def get_type(self, chemical_event):
        return "Appl. of " + chemical_event.get_type_display()

    def get_event_type(self, chemical_event):
        return CHEMICAL_EVENT_TYPE


class UpdateWeatherEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherEvent
        fields = "__all__"

    def to_internal_value(self, data):
        type = data.get("type", None)
        if type is None:
            raise serializers.ValidationError(
                {"type": ["This field is required."]}, code="required"
            )
        data = data.copy()
        extra_data = {}
        if type == WeatherEvent.FROST:
            extra_data["lower_temperature"] = data.pop("lower_temperature", None)
            extra_data["way_of_protection"] = data.pop("way_of_protection", None)
        elif type == WeatherEvent.DROUGHT:
            extra_data["water_deficit"] = data.pop("water_deficit", None)
        elif type == WeatherEvent.HAILSTORM:
            extra_data["weight"] = data.pop("weight", None)
            extra_data["diameter"] = data.pop("diameter", None)
            extra_data["duration"] = data.pop("duration", None)
            extra_data["way_of_protection"] = data.pop("way_of_protection", None)
        elif type == WeatherEvent.HIGH_TEMPERATURE:
            extra_data["highest_temperature"] = data.pop("highest_temperature", None)
            extra_data["start_date"] = data.pop("start_date", None)
            extra_data["end_date"] = data.pop("end_date", None)
        internal_value = super().to_internal_value(data)
        internal_value.extra_data = extra_data

        return internal_value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        type = data.get("type", None)
        if type == WeatherEvent.FROST:
            data["lower_temperature"] = instance.extra_data["lower_temperature"]
            data["way_of_protection"] = instance.extra_data["way_of_protection"]
        elif type == WeatherEvent.DROUGHT:
            data["water_deficit"] = instance.extra_data["water_deficit"]
        elif type == WeatherEvent.HAILSTORM:
            data["weight"] = instance.extra_data["weight"]
            data["diameter"] = instance.extra_data["diameter"]
            data["duration"] = instance.extra_data["duration"]
            data["way_of_protection"] = instance.extra_data["way_of_protection"]
        elif type == WeatherEvent.HIGH_TEMPERATURE:
            data["highest_temperature"] = instance.extra_data["highest_temperature"]
            data["start_date"] = instance.extra_data["start_date"]
            data["end_date"] = instance.extra_data["end_date"]
        data.pop("extra_data")
        return data

    def update(self, instance, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = instance.album
            if gallery is None:
                gallery = Gallery.objects.create()
            for image_data in album_data.getlist("album[images]"):
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().update(instance, validated_data)

    def create(self, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = Gallery.objects.create()
            for image_data in album_data.getlist("album[images]"):
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().create(validated_data)


class WeatherEventSerializer(EventSerializer):
    type = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField()

    class Meta:
        model = WeatherEvent
        fields = "__all__"

    def get_type(self, weather_event):
        return weather_event.get_type_display()

    def get_event_type(self, weather_event):
        return WEATHER_EVENT_TYPE


class UpdateProductionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionEvent
        fields = "__all__"


class ProductionEventSerializer(EventSerializer):
    type = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField()

    class Meta:
        model = ProductionEvent
        fields = "__all__"

    def get_type(self, production_event):
        return production_event.get_type_display()

    def get_event_type(self, production_event):
        return PRODUCTION_EVENT_TYPE


class UpdateGeneralEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralEvent
        fields = "__all__"


class GeneralEventSerializer(EventSerializer):
    type = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField()

    class Meta:
        model = GeneralEvent
        fields = "__all__"

    def get_type(self, general_event):
        return general_event.name

    def get_event_type(self, general_event):
        return GENERAL_EVENT_TYPE


class HistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    certificate_percentage = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    parcel = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = [
            "id",
            "start_date",
            "finish_date",
            "name",
            "published",
            "events",
            "earning",
            "parcel",
            "members",
            "certificate_percentage",
            "product",
            "qr_code",
            "reputation",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "certificate_percentage"]

    def get_product(self, history):
        return history.product.name if history.product else None

    def get_events(self, history):
        return history.get_events()

    def get_parcel(self, history):
        return history.parcel.name if history.parcel else None

    def get_certificate_percentage(self, history):
        return history.certificate_percentage

    def get_members(self, history):
        events = history.history_weatherevent_events.all()
        members = []
        for event in events:
            if event.created_by:
                members.append(
                    event.created_by.first_name + " " + event.created_by.last_name
                )
        return members[0:3]


class ListHistoryClassSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    parcel = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = HistoryScan
        fields = [
            "id",
            "date",
            "product",
            "location",
            "parcel",
            "comment",
        ]

    def get_date(self, history_scan):
        return history_scan.date.strftime("%m/%d/%Y")

    def get_product(self, history_scan):
        return (
            history_scan.history.product.name if history_scan.history.product else None
        )

    def get_location(self, history_scan):
        if history_scan.city is None and history_scan.country is None:
            return "-"
        elif history_scan.city is not None:
            return f"{history_scan.city}"
        elif history_scan.country is not None:
            return f"{history_scan.country}"
        return f"{history_scan.city if history_scan.city is not None else '-'}, {history_scan.country if history_scan.country is not None else '-'}"

    def get_parcel(self, history_scan):
        return history_scan.history.parcel.name if history_scan.history.parcel else None


class PublicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name"]


class PublicEstablishmentSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = ["name", "description", "location"]

    def get_location(self, establishment):
        return establishment.get_location()


class PublicParcelSerializer(serializers.ModelSerializer):
    establishment = PublicEstablishmentSerializer()

    class Meta:
        model = Parcel
        fields = ["name", "polygon", "map_metadata", "establishment"]


class PublicHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    certificate_percentage = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    parcel = PublicParcelSerializer()
    product = PublicProductSerializer()
    history_scan = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = [
            "id",
            "start_date",
            "finish_date",
            "name",
            "events",
            "certificate_percentage",
            "product",
            "reputation",
            "company",
            "parcel",
            "history_scan",
        ]

    def get_events(self, history):
        return history.get_events()

    def get_certificate_percentage(self, history):
        return history.certificate_percentage

    def get_company(self, history):
        return history.parcel.establishment.company.name if history.parcel else None

    def get_parcel(self, history):
        return history.parcel.name if history.parcel else None

    def get_history_scan(self, history):
        return self.context.get("history_scan", None)


class HistoryListOptionsSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ["id", "period"]

    def get_period(self, history):
        return f"{history.start_date.strftime('%m/%d/%Y')} - {history.finish_date.strftime('%m/%d/%Y')}"
