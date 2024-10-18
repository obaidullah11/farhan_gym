"""Models for Personal Training App"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User
from django.db import models
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip
import os
from PIL import Image
class Category(models.Model):
    """Category for exercises (e.g., Strength, Cardio, Flexibility)"""
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class Exercise(models.Model):
    """Exercise such as plank, squat, row"""
   
    name = models.CharField(max_length=40, unique=True)
    body_part = models.CharField(max_length=2,)
    instructions = models.CharField(max_length=40, blank=True)
    gif = models.FileField(upload_to='exercise_videos/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='exercises', null=True, blank=True)

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




