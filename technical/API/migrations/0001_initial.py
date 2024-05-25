# Generated by Django 4.2.13 on 2024-05-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Input",
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
                ("date", models.DateField()),
                ("invoice_number", models.IntegerField()),
                ("value", models.FloatField()),
                ("haircut", models.FloatField()),
                ("daily_fee", models.FloatField()),
                ("currency", models.TextField()),
                ("revenue_src", models.TextField()),
                ("customer", models.TextField()),
                ("expected_payment_duration", models.IntegerField()),
                ("epoch", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Result",
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
                ("revenue_src", models.TextField()),
                ("value", models.FloatField()),
                ("advance", models.FloatField()),
                ("expected_fee", models.FloatField()),
                ("epoch", models.IntegerField()),
            ],
        ),
    ]