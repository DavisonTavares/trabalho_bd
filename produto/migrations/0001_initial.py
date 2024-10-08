# Generated by Django 5.0.1 on 2024-08-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("nome", models.CharField(max_length=255)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("quantidade", models.PositiveIntegerField()),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                ("marca", models.CharField(max_length=255)),
                ("litragem", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
