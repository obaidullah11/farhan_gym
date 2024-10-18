from rest_framework import serializers
from .models import Workout, workoutExercise, Set, WorkoutSession, SetPerformance,Folder
from train.models import Exercise
from train.serializers import ExerciseSerializer
class FolderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'device_id']  # Added device_id to the fields

    def create(self, validated_data):
        # You can customize the folder creation logic as needed
        folder, created = Folder.objects.get_or_create(
            name=validated_data['name'], device_id=validated_data['device_id']
        )
        return folder
class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'set_number', 'kg', 'reps']

class workoutExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)

    class Meta:
        model = workoutExercise
        fields = ['exercise', 'order', 'sets']

class WorkoutSerializer(serializers.ModelSerializer):
    perform_exercises = workoutExerciseSerializer(many=True)
    folder = serializers.CharField(write_only=True)  # Expect folder name from the request

    class Meta:
        model = Workout
        fields = ['device_id', 'name', 'folder', 'perform_exercises']  # Include folder in fields

    def create(self, validated_data):
        perform_exercises_data = validated_data.pop('perform_exercises')
        folder_name = validated_data.pop('folder')  # Extract folder name from validated data

        # Get or create the folder by name
        folder, _ = Folder.objects.get_or_create(name=folder_name)

        # Create the workout and link it to the folder
        workout = Workout.objects.create(folder=folder, **validated_data)

        # Create the workout exercises and their sets
        for exercise_data in perform_exercises_data:
            sets_data = exercise_data.pop('sets')
            workout_exercise = workoutExercise.objects.create(workout=workout, **exercise_data)

            # Create sets for each workout exercise
            Set.objects.bulk_create(
                [Set(workoutExercise=workout_exercise, **set_data) for set_data in sets_data]
            )

        # Automatically create a workout session for the workout
        WorkoutSession.objects.create(device_id=workout.device_id, workout=workout)

        return workout

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['device_id'] = instance.device_id  # Show the device_id instead of user ID

        # Retrieve the associated folder
        representation['folder'] = instance.folder.name  # Add folder name to representation

        # Retrieve the associated WorkoutSession
        workout_session = WorkoutSession.objects.filter(workout=instance).first()
        representation['session_id'] = workout_session.id if workout_session else None  # Add session ID to representation

        for exercise in representation['perform_exercises']:
            exercise_id = exercise['exercise']
            try:
                exercise_obj = Exercise.objects.get(id=exercise_id)
                exercise['exercise'] = exercise_obj.name
            except Exercise.DoesNotExist:
                exercise['exercise'] = 'Unknown Exercise'

        return representation

class SetPerformanceSerializer(serializers.ModelSerializer):
    set = serializers.PrimaryKeyRelatedField(queryset=Set.objects.all())

    class Meta:
        model = SetPerformance
        fields = ['set', 'actual_kg', 'actual_reps']

class SetPerformanceSerializerNew(serializers.ModelSerializer):
    exercise = serializers.SerializerMethodField()

    class Meta:
        model = SetPerformance
        fields = ['id', 'actual_kg', 'actual_reps', 'exercise']

    def get_exercise(self, obj):
        return ExerciseSerializer(obj.set.workoutExercise.exercise).data 

class UpdateProgressSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    performances = serializers.ListField(
        child=serializers.DictField(
            child=serializers.FloatField()  # Ensure actual_kg and actual_reps are validated as floats
        )
    )

    def validate(self, attrs):
        session_id = attrs.get('session_id')
        performances = attrs.get('performances')

        # Validate the session ID
        if not WorkoutSession.objects.filter(id=session_id).exists():
            raise serializers.ValidationError(f"Session ID {session_id} does not exist.")

        # Validate each performance's set ID
        for performance in performances:
            set_id = performance['set']  # Access set ID
            
            # Convert to integer if it's a float
            if isinstance(set_id, float):
                set_id = int(set_id)

            if not isinstance(set_id, int) or not Set.objects.filter(id=set_id).exists():
                raise serializers.ValidationError(f"Set ID {set_id} does not exist.")

        return attrs
    
class FolderSerializernew(serializers.ModelSerializer):
    workouts = WorkoutSerializer(many=True, read_only=True)  # Nested serializer to include workouts

    class Meta:
        model = Folder
        fields = ['id', 'name', 'created_at', 'device_id', 'workouts']  # Include workouts in the fields
