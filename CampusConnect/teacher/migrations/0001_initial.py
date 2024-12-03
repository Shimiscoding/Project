# Generated by Django 5.1.1 on 2024-11-22 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=100)),
                ('father_occupation', models.CharField(blank=True, max_length=100)),
                ('father_mobile', models.CharField(max_length=15)),
                ('father_email', models.EmailField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_occupation', models.CharField(blank=True, max_length=100)),
                ('mother_mobile', models.CharField(max_length=15)),
                ('mother_email', models.EmailField(max_length=100)),
                ('present_address', models.TextField()),
                ('permanent_address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('Teacher_id', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('Teacher_class', models.CharField(max_length=50)),
                ('religion', models.CharField(max_length=50)),
                ('joining_date', models.DateField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('admission_number', models.CharField(max_length=20)),
                ('section', models.CharField(max_length=10)),
                ('Teacher_image', models.ImageField(blank=True, upload_to='Teachers/')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teacher.parent')),
            ],
        ),
    ]
