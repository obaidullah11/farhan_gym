# Generated by Django 3.2.10 on 2024-10-04 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0026_auto_20241004_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to=settings.AUTH_USER_MODEL),
        ),
    ]
