# Generated by Django 4.1.4 on 2023-09-12 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("history", "0012_chemicalevent_area_chemicalevent_commercial_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chemicalevent",
            name="name",
        ),
        migrations.RemoveField(
            model_name="productionevent",
            name="name",
        ),
        migrations.RemoveField(
            model_name="weatherevent",
            name="name",
        ),
    ]