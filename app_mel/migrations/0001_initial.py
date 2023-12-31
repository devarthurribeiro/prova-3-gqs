# Generated by Django 4.2.3 on 2023-07-12 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Criacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('raca', models.TextField(max_length=120)),
                ('data_entrada', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Coleta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('quantidade', models.DecimalField(decimal_places=3, max_digits=12)),
                ('criacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_mel.criacao')),
            ],
        ),
    ]
