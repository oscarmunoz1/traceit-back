from django.db import models
import qrcode


from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from product.models import Parcel


class History(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    earning = models.FloatField(default=0)
    lot_id = models.CharField(max_length=30, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    production_amount = models.FloatField(default=0)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)
    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="histories",
    )

    def save(self, *args, **kwargs):
        url = f"https://trood-back-staging.up.railway.app/admin/history/history/{self.id}/change/"
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

    def finish(self, history_data):
        print(history_data)
        self.finish_date = history_data["finish_date"]
        self.observation = history_data["observation"]
        self.published = True
        self.production_amount = history_data["production_amount"]
        self.lot_id = history_data["lot_id"]
        self.save()

    @property
    def certificate_percentage(self):
        events = self.history_weatherevent_events.all()
        if events.count() == 0:
            return 0
        certified_events = events.filter(certified=True).count()
        return int(certified_events / events.count() * 100)


class CommonEvent(models.Model):
    name = models.CharField(max_length=30)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.index = self.history.history_weatherevent_events.count() + 1
        super(CommonEvent, self).save(*args, **kwargs)

    def __str__(self):
        if self.history.parcel is not None:
            return (
                self.name
                + " - "
                + self.history.parcel.name
                + " - "
                + self.history.parcel.establishment.name
            )
        else:
            return self.name

    class Meta:
        abstract = True


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
    type = models.CharField(max_length=30)
    volume = models.FloatField(default=0)
    concentration = models.FloatField(default=0)
    time_period = models.CharField(max_length=30, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)


class GeneralEvent(CommonEvent):
    name = models.CharField(max_length=90)
    observation = models.TextField(blank=True, null=True)
