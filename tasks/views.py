from rest_framework import viewsets
from .models import Drink
from .serializers import DrinkSerializer
from .models import (
    Semester, Course, ClassMeeting, RoutinePreset,
    AcademicEvent, Task, Habit, HabitCheckin
)

from .serializers import (
    CourseSerializer, SemesterSerializer, ClassMeetingSerializer, TaskSerializer,
    RoutinePresetSerializer, AcademicEventSerializer, HabitCheckinSerializer,
    HabitSerializer
)

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ClassMeetingViewSet(viewsets.ModelViewSet):
    queryset = ClassMeeting.objects.all()
    serializer_class = ClassMeetingSerializer

class RoutinePresetViewSet(viewsets.ModelViewSet):
    queryset = RoutinePreset.objects.all()
    serializer_class = RoutinePresetSerializer

class AcademicEventViewSet(viewsets.ModelViewSet):
    queryset = AcademicEvent.objects.all()
    serializer_class = AcademicEventSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

class HabitCheckinViewSet(viewsets.ModelViewSet):
    queryset = HabitCheckin.objects.all()
    serializer_class = HabitCheckinSerializer