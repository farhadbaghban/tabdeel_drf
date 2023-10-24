# Generated by Django 4.1.5 on 2023-10-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("full_name", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone_number", models.CharField(max_length=11, unique=True)),
                ("id_card_number", models.CharField(max_length=10, unique=True)),
                (
                    "credit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "de_activate_date",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("registered_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "seller",
                "verbose_name_plural": "sellers",
                "ordering": ["credit", "full_name"],
            },
        ),
        migrations.CreateModel(
            name="DeletedUsers",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("accounts.user",),
        ),
    ]
