from rest_framework import serializers

from tasks.models import (
    Semester, Course, ClassMeeting, RoutinePreset,
    AcademicEvent, Task, Habit, HabitCheckin
)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class SemesterSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = Semester
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'courses']
    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError(
                "End date must be after Start date"
            )
        return data

class ClassMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMeeting
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError(
                "End date must be after Start date"
            )
        return data
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        if data.get('is_advanced') and (not data.get('start_at') or not data.get('end_at')):
                raise serializers.ValidationError(
                    "start_at and end_at are required when is_advanced is True"
                )
        return data
        
class RoutinePresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutinePreset
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

class AcademicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicEvent
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class HabitCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCheckin
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class HabitSerializer(serializers.ModelSerializer):
    checkins = HabitCheckinSerializer(many=True, read_only=True)
    current_streak = serializers.SerializerMethodField()
    best_streak = serializers.SerializerMethodField()
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

    def get_current_streak(self, obj):
        return obj.get_current_streak()

    def get_best_streak(self, obj):
        return obj.get_best_streak()

