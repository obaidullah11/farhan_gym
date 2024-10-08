from django.urls import path
from .views import *

urlpatterns = [
    # Exercise URLs
    path('exercises/', exercise_list_create, name='exercise-list-create'),
    path('exercises/<int:pk>/', exercise_detail, name='exercise-detail'),

    # Routine URLs
    path('routines/', routine_list_create, name='routine-list-create'),
    path('routines/<int:pk>/', routine_detail, name='routine-detail'),
    path('routines/client/<int:client_id>/', routine_by_client, name='routine-by-client'),

    # Session URLs
    path('sessions/', session_list_create, name='session-list-create'),
    path('sessions/<int:pk>/', session_detail, name='session-detail'),
    path('user/sessions/<int:user_id>/', user_sessions, name='session-detail'),


    # Setgroup URLs
    path('setgroups/', setgroup_list_create, name='setgroup-list-create'),
    path('setgroups/<int:pk>/',setgroup_detail, name='setgroup-detail'),

    # Set URLs
    path('sets/', set_list_create, name='set-list-create'),
    path('sets/<int:pk>/', set_detail, name='set-detail'),
]
