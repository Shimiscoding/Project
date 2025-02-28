# Generated by Django 5.1.1 on 2024-11-23 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parent',
            old_name='father_name',
            new_name='emergency_name',
        ),
        migrations.RenameField(
            model_name='parent',
            old_name='father_mobile',
            new_name='mobile',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='father_email',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='father_occupation',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='mother_email',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='mother_mobile',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='mother_name',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='mother_occupation',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='section',
        ),
    ]
