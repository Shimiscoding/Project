# Generated by Django 5.1.1 on 2024-11-29 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0019_alter_vote_unique_together_remove_votingoption_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votingoption',
            name='notification',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='upvotes',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.DeleteModel(
            name='VotingOption',
        ),
    ]
