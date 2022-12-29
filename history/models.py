from django.db import models
import qrcode

from product.models import Parcel

from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile


class History(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    description = models.TextField()
    published = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)

    def __str__(self):
        return self.name

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
            f"{self.name}-{self.date}.png", ContentFile(buf.getvalue()), save=False
        )

        super().save(*args, **kwargs)


class Event(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to="event_images", blank=True)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    certified = models.BooleanField(default=False)
    history = models.ForeignKey(
        History, on_delete=models.CASCADE, blank=True, null=True
    )
    index = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.index = self.history.event_set.count() + 1
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return (
            self.name
            + " - "
            + self.parcel.name
            + " - "
            + self.parcel.establishment.name
        )
