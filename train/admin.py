"""Models registered on Django Admin site"""
from django.contrib import admin
from .models import  Exercise, Routine, Setgroup, Set, Session
from django.utils.html import mark_safe



class SetInline(admin.TabularInline):
    model = Set

class SetgroupAdmin(admin.ModelAdmin):
    inlines = [
        SetInline
    ]

class SetgroupInline(admin.TabularInline):
    model = Setgroup

class SessionAdmin(admin.ModelAdmin):
    inlines = [
        SetgroupInline,
    ]

# admin.site.register(User)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part', 'gif_preview')

    def gif_preview(self, obj):
        """Display a preview of the video in the admin list."""
        if obj.gif:  # Check if a file exists
            return mark_safe(f'''
                <video width="100"  controls>
                    <source src="{obj.gif.url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            ''')  # Display the video
        return "No Video"

    gif_preview.short_description = 'GIF/Video Preview'

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Routine)
admin.site.register(Setgroup, SetgroupAdmin)
admin.site.register(Set)
admin.site.register(Session, SessionAdmin)
