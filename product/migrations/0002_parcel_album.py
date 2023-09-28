# Generated by Django 4.1.4 on 2023-09-01 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="parcel",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="common.gallery",
            ),
        ),
    ]