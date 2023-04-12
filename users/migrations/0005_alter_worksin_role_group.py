# Generated by Django 4.1.4 on 2023-04-04 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0004_alter_worksin_establishments_in_charge"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worksin",
            name="role_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth.group",
            ),
        ),
    ]