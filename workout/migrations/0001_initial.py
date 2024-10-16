# Generated by Django 5.0 on 2024-10-15 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('train', '0029_exercise_instructions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perform_exercises', to='train.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_number', models.PositiveIntegerField()),
                ('kg', models.DecimalField(decimal_places=2, max_digits=5)),
                ('reps', models.PositiveIntegerField()),
                ('perform_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='workout.performexercise')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='performexercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perform_exercises', to='workout.workout'),
        ),
        migrations.CreateModel(
            name='WorkoutSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_sessions', to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_sessions', to='workout.workout')),
            ],
        ),
        migrations.CreateModel(
            name='SetPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_kg', models.DecimalField(decimal_places=2, max_digits=5)),
                ('actual_reps', models.PositiveIntegerField()),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.set')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_performances', to='workout.workoutsession')),
            ],
        ),
    ]
