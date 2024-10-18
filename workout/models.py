from django.db import models
from train.models import Exercise
from django.core.exceptions import ValidationError

class Folder(models.Model):
    name = models.CharField(max_length=100)  # Field to store the folder name
    created_at = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=255)
      # Automatically set the timestamp when created

    def __str__(self):
        return self.name


class Workout(models.Model):
    device_id = models.CharField(max_length=255,null=True,blank=True)  # Use device_id instead of User
    name = models.CharField(max_length=255)  # Workout name (e.g., 'Leg Day', 'Push Day')
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='workouts')  # Link to Folder model
    def __str__(self):
        return f'{self.name} - {self.device_id}'


class workoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="perform_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="perform_exercises")  # Link to Exercise
    order = models.PositiveIntegerField(default=0)  # Order of the exercise in the workout

    def __str__(self):
        return f'{self.exercise.name} in {self.workout.name}'

    def clean(self):
        """Ensure that exercise order is not negative."""
        if self.order < 0:
            raise ValidationError("Order must be a non-negative value.")

class Set(models.Model):
    workoutExercise = models.ForeignKey(workoutExercise, on_delete=models.CASCADE, related_name="sets")
    set_number = models.PositiveIntegerField()  # Set number (e.g., Set 1, Set 2)
    kg = models.DecimalField(max_digits=5, decimal_places=2)  # Preset weight in kg
    reps = models.PositiveIntegerField()  # Preset number of repetitions

    def __str__(self):
        return f'{self.workoutExercise.exercise.name} - Set {self.set_number}: {self.kg}kg x {self.reps}'


# Track user performance for each workout session
class WorkoutSession(models.Model):
    device_id = models.CharField(max_length=255,null=True,blank=True)  # Use device_id instead of User
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workout_sessions")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} - {self.workout.name} on {self.date}'

# Track actual performance for each set in a workout session
class SetPerformance(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="set_performances")
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    actual_kg = models.DecimalField(max_digits=5, decimal_places=2)  # Actual weight lifted
    actual_reps = models.PositiveIntegerField()  # Actual reps performed

    def __str__(self):
        return f'{self.session.workout.name} - Set {self.set.set_number}: {self.actual_kg}kg x {self.actual_reps} reps'

    def clean(self):
        """Ensure actual values are logical."""
        if self.actual_kg < 0:
            raise ValidationError("Weight must be a positive value.")
        if self.actual_reps < 0:
            raise ValidationError("Reps must be a positive value.")
        if self.actual_kg > self.set.kg:
            raise ValidationError("Actual weight cannot exceed the set weight.")