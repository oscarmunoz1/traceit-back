# Generated by Django 4.1.4 on 2024-01-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_parcel_polygon"),
    ]

    operations = [
        migrations.AddField(
            model_name="parcel",
            name="map_metadata",
            field=models.JSONField(blank=True, null=True),
        ),
    ]