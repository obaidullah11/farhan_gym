from django.urls import path
from .views import ExerciseRecordsView,WorkoutHistoryByDeviceView, UpdateWorkoutView, CreateFolderView,CreateWorkoutView,FolderByDeviceIDView,get_user_workouts,UpdateWorkoutProgressView,GetSetPerformanceByUserView

urlpatterns = [
    path('workouts/create/', CreateWorkoutView.as_view(), name='create_workout'),
    path('user/<str:device_id>/workouts/', get_user_workouts, name='get_user_workouts'),
    path('api/workout/sessions/<str:device_id>/', GetSetPerformanceByUserView.as_view(), name='get-workout-sessions'),
    path('api/workout/update-progress/<str:device_id>/', UpdateWorkoutProgressView.as_view(), name='update-workout-progress'),
    path('api/folder/create/', CreateFolderView.as_view(), name='create-folder'),
    path('api/folders/<str:device_id>/', FolderByDeviceIDView.as_view(), name='folders-by-device-id'),
    path('api/workout/update/<int:pk>/', UpdateWorkoutView.as_view(), name='update-workout'),
    path('api/workout/history/<str:device_id>/', WorkoutHistoryByDeviceView.as_view(), name='workout-history-by-device'),
    path('exercise-records/<str:device_id>/<int:exercise_id>/', ExerciseRecordsView.as_view(), name='exercise-records'),
]
