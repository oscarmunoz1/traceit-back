# Generated by Django 4.1.4 on 2023-08-03 18:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("history", "0008_rename_observation_history_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="reputation",
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]