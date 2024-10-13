"""Models for Personal Training App"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User
from django.db import models
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip
import os
from PIL import Image

class Exercise(models.Model):
    """Exercise such as plank, squat, row"""
    body_choices = [
        ('LE', 'Legs'),
        ('AR', 'Arms'),
        ('BA', 'Back'),
        ('CH', 'Chest'),
        ('SH', 'Shoulders'),
        ('CO', 'Core'),
        ('OT', 'Other')
    ]
    name = models.CharField(max_length=40, unique=True)
    body_part = models.CharField(max_length=2, choices=body_choices)
    gif = models.FileField(upload_to='exercise_videos/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if a file is uploaded
        if self.gif:
            # Check file size (convert to MB)
            file_size = self.gif.size / (1024 * 1024)

            # Define the file path
            file_path = self.gif.path

            # If file size is greater than 2MB, compress
            if file_size > 2:
                # Handle video compression
                if file_path.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                    self.compress_video(file_path)

                # Handle GIF compression
                elif file_path.endswith('.gif'):
                    self.compress_gif(file_path)

        super().save(*args, **kwargs)

    def compress_video(self, file_path):
        """Compress video file to reduce size below 2MB."""
        # Open the video file using moviepy
        clip = VideoFileClip(file_path)

        # Compress the video to reduce file size
        # Here, we resize to a smaller resolution to reduce size
        clip_resized = clip.resize(height=360)  # Adjust height as needed to reduce file size

        # Save the compressed file to the same path (overwrite)
        compressed_path = file_path.replace(".mp4", "_compressed.mp4")  # Temporary save with new name
        clip_resized.write_videofile(compressed_path, bitrate="500k", codec='libx264')  # Save compressed

        # Replace the original file with the compressed file
        os.replace(compressed_path, file_path)

    def compress_gif(self, file_path):
        """Compress GIF file to reduce size below 2MB."""
        # Open the GIF using Pillow
        gif = Image.open(file_path)

        # Compress by reducing resolution or quality
        gif.thumbnail((480, 480))  # Adjust resolution to reduce size

        # Save the compressed GIF back
        compressed_path = file_path.replace(".gif", "_compressed.gif")  # Temporary save with new name
        gif.save(compressed_path, format='GIF', optimize=True, quality=85)

        # Replace the original file with the compressed file
        os.replace(compressed_path, file_path)




# class Exercise(models.Model):
#     """Exercise such as plank, squat, row"""
#     body_choices = [
#         ('LE', 'Legs'),
#         ('AR', 'Arms'),
#         ('BA', 'Back'),
#         ('CH', 'Chest'),
#         ('SH', 'Shoulders'),
#         ('CO', 'Core'),
#         ('OT', 'Other')
#     ]
#     name = models.CharField(max_length=40, unique=True)
#     body_part = models.CharField(max_length=2, choices=body_choices)

#     def __str__(self):
#         return self.name

class Routine(models.Model):
    """A group of exercises for a particular user"""
    name = models.CharField(max_length=20, verbose_name='Routine Name')
    startdate = models.DateField(auto_now_add=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routines")
    exercises = models.ManyToManyField("Exercise", related_name="routines")
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.first_name}'s {self.name}"

class Setgroup(models.Model):
    """Series of sets for a specicic excercise in a specific routine"""
    exercise = models.ForeignKey("Exercise", on_delete=models.PROTECT, related_name="setgroups")
    session = models.ForeignKey("Session", on_delete=models.CASCADE, related_name="setgroups")
    note = models.CharField(max_length=50, blank=True, null=True)
    order = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.name} Sets"

class Set(models.Model):
    """One set of an exercise performed by one user one time"""
    num_choices = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    ]
    setgroup = models.ForeignKey("Setgroup", on_delete=models.CASCADE, related_name="sets")
    setnum = models.IntegerField(choices=num_choices, verbose_name='Set')
    weight = models.CharField(max_length=20)
    time = models.CharField(max_length=15)

    def __str__(self):
        return f"set {self.setnum} of {self.setgroup.exercise.name}"

    def serialize(self):
        """serialize Sets for API request"""
        return {
            "date": self.setgroup.session.timestamp.astimezone().strftime("%b %-d %Y, %-I:%M %p"),
            "weight": self.weight,
            "time": self.time
        }

class Session(models.Model):
    """A collection of setgroups by a user on a given day (e.g. a workout)"""
    routine = models.ForeignKey("Routine", on_delete=models.PROTECT, related_name="sessions",
                                limit_choices_to={'archived': 'False'})
    timestamp = models.DateTimeField(auto_now_add=True)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)

    def __str__(self):
        return f"Session {self.pk} by {self.trainer.first_name} - {self.routine.name}"

    
