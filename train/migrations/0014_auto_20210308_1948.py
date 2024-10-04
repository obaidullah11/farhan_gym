# Generated by Django 3.1.7 on 2021-03-08 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0013_auto_20210308_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='routine',
            field=models.ForeignKey(limit_choices_to={'archived': 'False'}, on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='train.routine'),
        ),
    ]
