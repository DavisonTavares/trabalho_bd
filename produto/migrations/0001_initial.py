# Generated by Django 5.0.1 on 2024-10-22 01:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('nomeFormatado', models.CharField(editable=False, max_length=255)),
                ('quantidade', models.PositiveIntegerField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('litragem', models.DecimalField(decimal_places=2, max_digits=5)),
                ('local_de_fabricacao', models.CharField(blank=True, default='Brasil', max_length=255, null=True)),
                ('url_imagem', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produto.marca')),
            ],
        ),
    ]
