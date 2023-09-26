from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=30)
    tradename = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    fiscal_id = models.CharField(max_length=30, help_text="RUT", blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos", blank=True)
    description = models.TextField(blank=True, null=True)
    invitation_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company-detail", kwargs={"id": self.id})


class Establishment(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30, blank=True, null=True)
    zone = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="establishment_images", blank=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _("Establishment")
        verbose_name_plural = _("Establishments")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("establishment-detail", kwargs={"id": self.id})
