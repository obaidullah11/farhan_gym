# Generated by Django 4.0.6 on 2024-10-23 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0012_setperformance_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sethistory',
            name='pr',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sethistory',
            name='rm',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
