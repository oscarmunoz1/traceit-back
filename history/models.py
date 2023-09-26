import qrcode
from io import BytesIO
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.files.base import ContentFile


from product.models import Parcel


class History(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    earning = models.FloatField(default=0)
    lot_id = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    production_amount = models.FloatField(default=0)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)
    reputation = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="histories",
    )
    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="histories",
    )

    def __str__(self) -> str:
        return (
            "[ "
            + str(self.start_date.strftime("%m/%d/%Y"))
            + " - "
            + str(self.finish_date.strftime("%m/%d/%Y"))
            if self.finish_date
            else "" + " ]" + " - " + self.product.name
            if self.product
            else ""
        )

    def update_reputation(self):
        average_reputation = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        if average_reputation is not None:
            self.reputation = round(average_reputation, 2)
        else:
            # If there are no reviews, the default reputation is 0
            self.reputation = 0.00
        self.save()

    def save(self, *args, **kwargs):
        url = f"https://localhost:3000/history/{self.id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to a BytesIO object
        buf = BytesIO()
        img.save(buf)

        # Set the `qr_code` field to be the contents of the BytesIO object
        self.qr_code.save(
            f"{self.name}-{self.start_date}.png",
            ContentFile(buf.getvalue()),
            save=False,
        )

        super().save(*args, **kwargs)

    @property
    def certificate_percentage(self):
        events = self.history_weatherevent_events.all()
        if events.count() == 0:
            return 0
        certified_events = events.filter(certified=True).count()
        return int(certified_events / events.count() * 100)

    def finish(self, history_data):
        self.finish_date = history_data["finish_date"]
        self.observation = history_data["observation"]
        self.published = True
        self.production_amount = history_data["production_amount"]
        self.lot_id = history_data["lot_id"]
        self.save()

    def get_events(self):
        from .serializers import (
            WeatherEventSerializer,
            ChemicalEventSerializer,
            ProductionEventSerializer,
            GeneralEventSerializer,
        )

        events = (
            WeatherEventSerializer(
                self.history_weatherevent_events.all(), many=True
            ).data
            + ChemicalEventSerializer(
                self.history_chemicalevent_events.all(), many=True
            ).data
            + ProductionEventSerializer(
                self.history_productionevent_events.all(), many=True
            ).data
            + GeneralEventSerializer(
                self.history_generalevent_events.all(), many=True
            ).data
        )
        return sorted(events, key=lambda event: event["index"])


class CommonEvent(models.Model):
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to="event_images", blank=True)
    certified = models.BooleanField(default=False)
    history = models.ForeignKey(
        History,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_events",
    )
    index = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.index = (
                self.history.history_weatherevent_events.count()
                + self.history.history_chemicalevent_events.count()
                + self.history.history_generalevent_events.count()
                + self.history.history_productionevent_events.count()
            ) + 1
        super(CommonEvent, self).save(*args, **kwargs)

    def __str__(self) -> str:
        if self.history.parcel is not None:
            return (
                self.history.parcel.name
                + " - "
                + self.history.parcel.establishment.name
            )
        else:
            return self.history.name


class WeatherEvent(CommonEvent):
    FROST = "FR"
    DROUGHT = "DR"
    HEAT_WAVE = "HW"
    TROPICAL_STORM = "TS"
    HIGH_WINDS = "HW"
    HIGH_HUMIDITY = "HH"
    LOW_HUMIDITY = "LH"

    WEATHER_EVENTS = (
        (FROST, "Frost"),
        (DROUGHT, "Drought"),
        (HEAT_WAVE, "Heat Wave"),
        (TROPICAL_STORM, "Tropical Storm"),
        (HIGH_WINDS, "High Winds"),
        (HIGH_HUMIDITY, "High Humidity"),
        (LOW_HUMIDITY, "Low Humidity"),
    )

    type = models.CharField(
        max_length=2,
        choices=WEATHER_EVENTS,
    )
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    time_period = models.CharField(max_length=30, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)


class ChemicalEvent(CommonEvent):
    FERTILIZER = "FE"
    PESTICIDE = "PE"
    FUNGICIDE = "FU"
    HERBICIDE = "HE"

    CHEMICAL_EVENTS = (
        (FERTILIZER, "Fertilizer"),
        (PESTICIDE, "Pesticide"),
        (FUNGICIDE, "Fungicide"),
        (HERBICIDE, "Herbicide"),
    )

    type = models.CharField(
        max_length=2, choices=CHEMICAL_EVENTS, blank=True, null=True
    )
    commercial_name = models.CharField(max_length=60, blank=True, null=True)
    volume = models.FloatField(default=0)
    concentration = models.FloatField(default=0)
    area = models.FloatField(default=0, blank=True, null=True)
    way_of_application = models.CharField(max_length=30, blank=True, null=True)
    time_period = models.CharField(max_length=30, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)


class ProductionEvent(CommonEvent):
    PLANTING = "PL"
    HARVESTING = "HA"
    IRRIGATION = "IR"
    PRUNING = "PR"

    PRODUCTION_EVENTS = (
        (PLANTING, "Planting"),
        (HARVESTING, "Harvesting"),
        (IRRIGATION, "Irrigation"),
        (PRUNING, "Pruning"),
    )

    type = models.CharField(max_length=2, choices=PRODUCTION_EVENTS)
    observation = models.TextField(blank=True, null=True)


class GeneralEvent(CommonEvent):
    name = models.CharField(max_length=90)
    observation = models.TextField(blank=True, null=True)


class HistoryScan(models.Model):
    history = models.ForeignKey(
        History,
        on_delete=models.CASCADE,
        related_name="history_scans",
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, blank=True, null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
