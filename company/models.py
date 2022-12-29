from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30)
    tradename = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    fiscal_id = models.CharField(max_length=30, help_text="RUT")
    logo = models.ImageField(upload_to="company_logos", blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Establishment(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30, blank=True, null=True)
    zone = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="establishment_images", blank=True)

    def __str__(self):
        return self.name
