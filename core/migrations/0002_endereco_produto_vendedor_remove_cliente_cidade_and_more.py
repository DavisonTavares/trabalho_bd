# Generated by Django 5.0.1 on 2024-08-23 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('nome', models.CharField(max_length=255)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.PositiveIntegerField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marca', models.CharField(max_length=255)),
                ('litragem', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('nome', models.CharField(max_length=255)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='profissao',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=14, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='cliente',
            name='endereco',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.endereco'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_venda', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.PositiveIntegerField()),
                ('valor_prod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.produto')),
                ('id_vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vendedor')),
            ],
        ),
    ]
