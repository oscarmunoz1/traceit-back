# Generated by Django 4.1.4 on 2023-08-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("history", "0009_history_reputation"),
    ]

    operations = [
        migrations.AddField(
            model_name="historyscan",
            name="comment",
            field=models.TextField(blank=True, null=True),
        ),
    ]