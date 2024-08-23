# Generated by Django 5.0.1 on 2024-08-23 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("endereco", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
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
                ("nome", models.CharField(max_length=255)),
                ("cpf", models.CharField(max_length=14, unique=True)),
                ("telefone", models.CharField(max_length=20)),
                (
                    "endereco",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="endereco.endereco",
                    ),
                ),
            ],
        ),
    ]