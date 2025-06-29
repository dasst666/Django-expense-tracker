# Generated by Django 5.2.2 on 2025-06-24 10:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='main_catego_name_5111b9_idx')],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('income_type', models.CharField(choices=[('income', 'Доход'), ('expense', 'Расход')], default='expense', max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='main.category')),
            ],
            options={
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='main_transa_name_0c274b_idx'), models.Index(fields=['-created'], name='main_transa_created_436437_idx')],
            },
        ),
    ]
