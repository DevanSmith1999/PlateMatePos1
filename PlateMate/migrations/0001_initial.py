# Generated by Django 5.0.2 on 2024-03-25 23:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MenuItem",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("type", models.CharField(max_length=50, verbose_name="type")),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
