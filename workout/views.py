from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Workout, WorkoutSession, SetPerformance, Workout, workoutExercise, Set, SetPerformance,Folder
from .serializers import FolderSerializernew,FolderSerializer, WorkoutSerializer, UpdateProgressSerializer, SetPerformanceSerializerNew


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
    serializer = WorkoutSerializer(workouts, many=True)
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
    def post(self, request, device_id, *args, **kwargs):
        # Logging the incoming request data
        print("Incoming request data:", request.data)

        # Initialize the serializer with the data
        serializer = UpdateProgressSerializer(data=request.data)
        
        # Check if the serializer data is valid
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)  # Debugging invalid serializer data
            return Response({
                "status": False,
                "message": "Invalid data.",
                "data": serializer.errors  # Return errors if invalid data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log validated data
        print("Validated data:", serializer.validated_data)
        
        # Extract validated fields
        session_id = serializer.validated_data['session_id']
        performances = serializer.validated_data['performances']

        print(f"Device ID from URL: {device_id}, Session ID: {session_id}")
        
        # Try to get the workout session
        try:
            workout_session = WorkoutSession.objects.get(id=session_id, device_id=device_id)
        except WorkoutSession.DoesNotExist:
            print("Workout session not found for this device.")  # Debugging
            return Response({
                "status": False,
                "message": "Workout session not found for this device.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        print("Workout session found.")  # Debugging information

        # Iterate over the performance data and create/update SetPerformance records
        updated_performances = []
        for performance in performances:
            set_id = performance['set']
            actual_kg = performance['actual_kg']
            actual_reps = performance['actual_reps']

            # Create or update the SetPerformance record
            set_performance, created = SetPerformance.objects.update_or_create(
                session=workout_session,
                set_id=set_id,
                defaults={'actual_kg': actual_kg, 'actual_reps': actual_reps}
            )

            # Add the updated performance to the response data
            updated_performances.append({
                'set_id': set_id,
                'actual_kg': set_performance.actual_kg,
                'actual_reps': set_performance.actual_reps,
                'created': created
            })

        # Prepare the response data, including the updated performances
        response_data = {
            "status": True,
            "message": "Progress updated successfully.",
            "data": updated_performances  # Return the updated data
        }

        print("Returning success response with data:", response_data)  # Debugging final response

        # Return success response with the updated performance data
        return Response(response_data, status=status.HTTP_201_CREATED)
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
