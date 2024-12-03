# Generated by Django 5.1.1 on 2024-11-24 16:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_notification_options_notification_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
