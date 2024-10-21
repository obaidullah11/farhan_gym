from rest_framework import status, generics
from rest_framework.response import Response
from decimal import Decimal
from rest_framework.views import APIView
from django.db.models import Max
from rest_framework.decorators import api_view
from .models import Workout, WorkoutSession, SetPerformance, Workout, workoutExercise, Set, SetPerformance,Folder,WorkoutHistory,SetHistory
from .serializers import WorkoutHistorySerializer,WorkoutSerializernew,FolderSerializernew,FolderSerializer, WorkoutSerializer, UpdateProgressSerializer, SetPerformanceSerializerNew
from datetime import timedelta

class FolderByDeviceIDView(generics.ListAPIView):
    def get(self, request, device_id, *args, **kwargs):
        # Fetch all folders associated with the given device_id
        folders = Folder.objects.filter(device_id=device_id)

        if not folders.exists():
            return Response({
                "status": False,
                "message": "No folders found for this device.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        # Prepare the data response
        folder_data = []
        for folder in folders:
            folder_dict = {
                "id": folder.id,
                "name": folder.name,
                "created_at": folder.created_at,
                "device_id": folder.device_id,
                "workouts": []
            }

            # Fetch workouts under each folder
            workouts = Workout.objects.filter(folder=folder)
            for workout in workouts:
                workout_dict = {
                    "id": workout.id,
                    "name": workout.name,
                    "created_at": workout.created_at,
                    "perform_exercises": []
                }

                # Fetch exercises related to the workout
                exercises = workoutExercise.objects.filter(workout=workout)
                for exercise in exercises:
                    exercise_dict = {
                        "exercise_id": exercise.exercise.id,
                        "exercise_name": exercise.exercise.name,
                        "order": exercise.order,
                        "sets": []
                    }

                    # Fetch sets related to each exercise
                    sets = Set.objects.filter(workoutExercise=exercise)
                    for workout_set in sets:
                        set_dict = {
                            "set_id": workout_set.id,
                            "set_number": workout_set.set_number,
                            "kg": workout_set.kg,
                            "reps": workout_set.reps,
                            "previous_performance": {}
                        }

                        # Fetch the previous performance for the set
                        previous_performance = SetPerformance.objects.filter(set=workout_set).order_by('-session__date').first()

                        if previous_performance:
                            set_dict["previous_performance"] = {
                                "actual_kg": previous_performance.actual_kg,
                                "actual_reps": previous_performance.actual_reps
                            }

                        exercise_dict["sets"].append(set_dict)

                    workout_dict["perform_exercises"].append(exercise_dict)

                folder_dict["workouts"].append(workout_dict)

            folder_data.append(folder_dict)

        # Return the folder data with workouts, exercises, and previous performance data
        return Response({
            "status": True,
            "message": "Folders and associated workouts with previous performance data retrieved successfully.",
            "data": folder_data
        }, status=status.HTTP_200_OK)




# class FolderByDeviceIDView(generics.ListAPIView):
#     serializer_class = FolderSerializernew

#     def get(self, request, device_id, *args, **kwargs):
#         # Fetch folders by device_id
#         folders = Folder.objects.filter(device_id=device_id)

#         # If no folders are found, return a 404 response
#         if not folders.exists():
#             return Response({
#                 "status": False,
#                 "message": "No folders found for this device.",
#                 "data": []
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Serialize the folder data
#         serializer = FolderSerializernew(folders, many=True)
#         return Response({
#             "status": True,
#             "message": "Folders retrieved successfully.",
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)

class CreateFolderView(generics.CreateAPIView):
    serializer_class = FolderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        folder = serializer.save()

        return Response({
            "status": True,
            "message": "Folder created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
class CreateWorkoutView(APIView):
    def post(self, request, *args, **kwargs):
        print(f"Request Data: {request.data}")  # Debugging print
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Workout created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        print(f"Errors: {serializer.errors}")  # Debugging print
        return Response({
            "status": False,
            "message": "Failed to create workout.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_workouts(request, device_id):
    # Fetch workouts related to the device_id directly
    workouts = Workout.objects.filter(device_id=device_id)

    # If no workouts are found, return a 404 response
    if not workouts.exists():
        return Response({
            "status": False,
            "message": "No workouts found for this device.",
            "data": []
        }, status=status.HTTP_404_NOT_FOUND)

    # Serialize the workout data
    serializer = WorkoutSerializernew(workouts, many=True)
    serialized_workouts = serializer.data

    # Add previous performance data to each workout's exercises
    for workout in serialized_workouts:
        session_id = workout.get('session_id')

        for exercise in workout['perform_exercises']:
            for set_data in exercise['sets']:
                set_id = set_data['id']

                # Get the last SetPerformance record for this session and set
                set_performance = SetPerformance.objects.filter(session__id=session_id, set__id=set_id).last()

                if set_performance:
                    # If a performance is found, add the performance data under 'previous'
                    set_data['previous'] = {
                        'actual_kg': set_performance.actual_kg,
                        'actual_reps': set_performance.actual_reps
                    }
                else:
                    # No performance data found
                    set_data['previous'] = {}

    # Debugging info
    print(f"Device ID: {device_id}, Number of workouts: {workouts.count()}")

    return Response({
        "status": True,
        "message": "User workouts retrieved successfully.",
        "data": serialized_workouts
    }, status=status.HTTP_200_OK)

class UpdateWorkoutProgressView(generics.CreateAPIView):
    serializer_class = UpdateProgressSerializer  # Specify the serializer class

    def post(self, request, device_id, *args, **kwargs):
        # Initialize the serializer with the data
        serializer = self.get_serializer(data=request.data)

        # Validate the serializer data
        if not serializer.is_valid():
            return Response({"status": False, "message": "Invalid data.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        session_id = serializer.validated_data['session_id']
        performances = serializer.validated_data['performances']
        workout_time_str = request.data.get('workout_time')  # Get the workout time from the request

        # Convert workout_time string to timedelta
        workout_time = self.parse_workout_time(workout_time_str)

        # Try to get the workout session
        workout_session = WorkoutSession.objects.filter(id=session_id, device_id=device_id).first()
        if not workout_session:
            return Response({"status": False, "message": "Workout session not found."}, status=status.HTTP_404_NOT_FOUND)

        highest_weight = 0
        best_performance_set = None

        # Iterate over performances and update SetPerformance records
        for performance in performances:
            set_id = performance['set']
            actual_kg = performance['actual_kg']
            actual_reps = performance['actual_reps']

            # Update or create the SetPerformance record
            set_performance, created = SetPerformance.objects.update_or_create(
                session=workout_session,
                set_id=set_id,
                defaults={'actual_kg': actual_kg, 'actual_reps': actual_reps}
            )

            # Track the highest weight lifted
            if actual_kg > highest_weight:
                highest_weight = actual_kg
                best_performance_set = set_performance

        # Ensure the workout session exists before creating workout history
        if not best_performance_set:
            return Response({"status": False, "message": "No valid performances found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a workout history record
        workout_history = WorkoutHistory.objects.create(
            device_id=device_id,
            workout=workout_session.workout,
            session=workout_session,
            highest_weight=highest_weight,
            best_performance_set=best_performance_set,
            workout_time=workout_time  # Store the workout time
        )

        # Now create SetHistory records
        set_history_data = []
        for performance in performances:
            set_id = performance['set']
            actual_kg = performance['actual_kg']
            actual_reps = performance['actual_reps']

            workout_set = Set.objects.get(id=set_id)

            set_history = SetHistory.objects.create(
                workout_history=workout_history,  # Link to the created workout history
                exercise=workout_set.workoutExercise.exercise,
                set_number=workout_set.set_number,
                actual_kg=actual_kg,
                actual_reps=actual_reps
            )
            # Collect the data for response
            set_history_data.append({
                "exercise": workout_set.workoutExercise.exercise.name,
                "set_number": workout_set.set_number,
                "actual_kg": actual_kg,
                "actual_reps": actual_reps
            })

        # Prepare response data
        response_data = {
            "status": True,
            "message": "Progress updated successfully.",
            "workout_name": workout_session.workout.name,
            "date_time": workout_history.created_at.isoformat(),  # Get created_at from WorkoutHistory
            "total_weight": highest_weight,  # Use the highest weight tracked
            "workout_time": str(workout_time),  # Include the workout time in response
            "exercise_details": set_history_data
        }

        # Return a success response with workout history data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def parse_workout_time(self, time_str):
        """Convert a time string in the format HH:MM:SS to a timedelta."""
        if time_str:
            hours, minutes, seconds = map(int, time_str.split(':'))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return timedelta() 

class GetSetPerformanceByUserView(generics.ListAPIView):
    serializer_class = SetPerformanceSerializerNew

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        # Get all workout sessions for the user
        workout_sessions = WorkoutSession.objects.filter(user_id=user_id)

        # Check if the user has workout sessions
        if not workout_sessions.exists():
            return SetPerformance.objects.none()

        # Return all SetPerformance objects related to the user's workout sessions
        return SetPerformance.objects.filter(session__in=workout_sessions)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                "status": False,
                "message": "No set performances found for this user.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Set performances retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class UpdateWorkoutView(APIView):
    def put(self, request, *args, **kwargs):
        workout_id = kwargs.get('pk')  # Get the workout ID from the URL

        try:
            workout = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return Response({
                "status": False,
                "message": "Workout not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkoutSerializernew(workout, data=request.data, partial=True)  # Enable partial update

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Workout updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "Failed to update workout.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class WorkoutHistoryByDeviceView(generics.ListAPIView):
    serializer_class = WorkoutHistorySerializer

    def get_queryset(self):
        device_id = self.kwargs.get('device_id')
        return WorkoutHistory.objects.filter(device_id=device_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "No workout history found for this device."}, status=status.HTTP_404_NOT_FOUND)


import calendar
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum

class ExerciseRecordsView(generics.GenericAPIView):
    serializer_class = WorkoutHistorySerializer

    def get(self, request, device_id, exercise_id):
        # Get all workout histories for the given device_id and exercise_id
        workout_histories = WorkoutHistory.objects.filter(
            device_id=device_id, 
            session__set_performances__set__workoutExercise__exercise_id=exercise_id
        ).distinct()  # Ensure distinct workout histories

        # Initialize response structure
        response_data = {
            "status": True,
            "data": {
                "history": [],
                "records": {
                    "max_weight": 0,
                    "max_volume": 0,
                    "record_history": []
                },
                "monthly_charts": [],  # To store monthly aggregated data
                "weekly_charts": []  # To store weekly aggregated data
            }
        }

        # Prepare the history and records data
        for workout_history in workout_histories:
            # Prepare history details for a unique workout
            history_data = {
                "workout_name": workout_history.workout.name,
                "performed_time": workout_history.created_at,  # Include performed time
                "sets": []
            }

            # Get the sets performed against the workout history
            set_performances = SetPerformance.objects.filter(
                session=workout_history.session,
                set__workoutExercise__exercise_id=exercise_id
            )

            for set_performance in set_performances:
                history_data["sets"].append({
                    "set_number": set_performance.set.set_number,
                    "actual_kg": set_performance.actual_kg,
                    "actual_reps": set_performance.actual_reps,
                })

            # Append history data to response
            response_data["data"]["history"].append(history_data)

            # Prepare records data
            max_weight = set_performances.aggregate(Max('actual_kg'))['actual_kg__max'] or 0
            max_volume = sum(set_performance.actual_kg * set_performance.actual_reps for set_performance in set_performances)

            # Update collective max_weight and max_volume
            response_data["data"]["records"]["max_weight"] = max(
                response_data["data"]["records"]["max_weight"], 
                max_weight
            )
            response_data["data"]["records"]["max_volume"] += max_volume

            # Prepare detailed record history
            for set_performance in set_performances:
                predicted_weight = self.predict_weight(set_performance)  # Use the updated method
                response_data["data"]["records"]["record_history"].append({
                    "exercise": set_performance.set.workoutExercise.exercise.name,
                    "set_number": set_performance.set.set_number,
                    "actual_kg": set_performance.actual_kg,
                    "actual_reps": set_performance.actual_reps,
                    "predicted_weight": predicted_weight
                })

        # Add monthly and weekly chart data
        self.add_monthly_chart_data(response_data, workout_histories)
        self.add_weekly_chart_data(response_data, workout_histories)

        return Response(response_data)

    def predict_weight(self, set_performance):
        # Predict weight logic
        return set_performance.actual_kg * Decimal('1.1')  # Predicting a 10% increase

    def add_monthly_chart_data(self, response_data, workout_histories):
        # Aggregate monthly data for each exercise
        months = {}
        for workout_history in workout_histories:
            # Get the month and year for the workout
            month_year = workout_history.created_at.strftime('%Y-%m')
            if month_year not in months:
                months[month_year] = {
                    "month": month_year,
                    "total_weight": 0,
                    "total_reps": 0
                }

            # Sum the total weight and reps for the month
            set_performances = SetPerformance.objects.filter(session=workout_history.session)
            for set_performance in set_performances:
                months[month_year]["total_weight"] += set_performance.actual_kg
                months[month_year]["total_reps"] += set_performance.actual_reps

        # Append monthly data to the response
        response_data["data"]["monthly_charts"] = list(months.values())

    def add_weekly_chart_data(self, response_data, workout_histories):
        # Aggregate weekly data for each exercise
        weeks = {}
        current_date = now().date()
        for workout_history in workout_histories:
            # Calculate the start of the week (Monday)
            week_start = (workout_history.created_at - timedelta(days=workout_history.created_at.weekday())).date()
            if week_start not in weeks:
                weeks[week_start] = {
                    "week_start": str(week_start),
                    "total_weight": 0,
                    "total_reps": 0
                }

            # Sum the total weight and reps for the week
            set_performances = SetPerformance.objects.filter(session=workout_history.session)
            for set_performance in set_performances:
                weeks[week_start]["total_weight"] += set_performance.actual_kg
                weeks[week_start]["total_reps"] += set_performance.actual_reps

        # Append weekly data to the response
        response_data["data"]["weekly_charts"] = list(weeks.values())
