from django.db import models

from company.models import Establishment


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images", blank=True)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    album = models.ForeignKey(
        "common.Gallery", on_delete=models.CASCADE, blank=True, null=True
    )
    establishment = models.ForeignKey(
        Establishment, on_delete=models.CASCADE, related_name="parcels"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True
    )
    area = models.FloatField(help_text="Parcel area in hectares")
    certified = models.BooleanField(
        default=False, help_text="Certified by a professional"
    )
    current_history = models.OneToOneField(
        "history.History",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="current_parcel",
    )

    def __str__(self):
        return str(self.id) + " - " + self.name + " - " + self.establishment.name

    def finish_current_history(self, history_data):
        if self.current_history is not None:
            self.current_history.finish(history_data)
            history = self.current_history
            self.current_history = None
            self.save()
            return history
        return None
