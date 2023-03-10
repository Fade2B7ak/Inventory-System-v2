# Generated by Django 4.1.6 on 2023-02-10 10:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemClass', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('stock_date', models.DateField(auto_now_add=True)),
                ('ready_to_load', models.BooleanField(default=False)),
                ('cost_per_piece', models.IntegerField(default=True)),
            ],
        ),
    ]
