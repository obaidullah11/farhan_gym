# Generated by Django 5.0 on 2024-10-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0008_workouthistory_sethistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutsession',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
