# Generated by Django 4.1.4 on 2023-04-11 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("history", "0001_initial"),
        ("company", "0005_alter_company_tradename"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("description", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, upload_to="product_images")),
            ],
        ),
        migrations.CreateModel(
            name="Parcel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("description", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, upload_to="parcel_images")),
                ("area", models.FloatField(help_text="Parcel area in hectares")),
                (
                    "certified",
                    models.BooleanField(
                        default=False, help_text="Certified by a professional"
                    ),
                ),
                (
                    "current_history",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="current_parcel",
                        to="history.history",
                    ),
                ),
                (
                    "establishment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parcels",
                        to="company.establishment",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
            ],
        ),
    ]
