# Generated by Django 5.1.1 on 2024-12-02 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants_count',
            field=models.IntegerField(default=0),
        ),
    ]
