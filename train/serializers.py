from rest_framework import serializers
from .models import Exercise, Routine, Setgroup, Set, Session

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'gif']  # Include the gif field

    def validate_gif(self, value):
        """Check file size limit for gif uploads."""
        if value.size > 2 * 1024 * 1024:  # 2 MB limit
            raise serializers.ValidationError("File size should be less than 2MB.")
        return value
    

class RoutineSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Exercise.objects.all()
    )

    class Meta:
        model = Routine
        fields = ['id', 'name', 'client', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        routine = Routine.objects.create(**validated_data)
        routine.exercises.set(exercises_data)  # Assign the exercises using their IDs
        return routine
class newRoutineSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)  # Use the ExerciseSerializer for nested representation

    class Meta:
        model = Routine
        fields = ['id', 'name', 'client', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        routine = Routine.objects.create(**validated_data)
        
        # Create and assign exercises (if they are new) or just link existing ones
        for exercise_data in exercises_data:
            exercise, created = Exercise.objects.get_or_create(**exercise_data)
            routine.exercises.add(exercise)
        
        return routine



class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'setgroup', 'setnum', 'weight', 'time']




# class SessionSerializer(serializers.ModelSerializer):
#     setgroups = SetgroupSerializer(many=True)

#     class Meta:
#         model = Session
#         fields = ['id', 'routine', 'timestamp', 'trainer', 'setgroups']
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'routine', 'timestamp', 'trainer']
        read_only_fields = ['timestamp']  # Make timestamp read-only, as it's auto-generated

    def to_representation(self, instance):
        """Customizes the output representation of the session."""
        representation = super().to_representation(instance)
        representation['routine_name'] = instance.routine.name  # Include routine name
        representation['trainer_name'] = instance.trainer.username if instance.trainer else 'No Trainer'  # Include trainer name
        return representation
    
class SetgroupSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)
    exercise = ExerciseSerializer(many=True)
    session = SessionSerializer(many=True)

    class Meta:
        model = Setgroup
        fields = ['id', 'exercise', 'session', 'note', 'order', 'sets']