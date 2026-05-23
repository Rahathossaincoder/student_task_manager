from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import (
    Semester,
    Course,
    ClassMeeting,
    RoutinePreset,
    AcademicEvent,
    Task,
    Habit,
    HabitCheckin,
)

from .serializers import (
    CourseSerializer,
    SemesterSerializer,
    ClassMeetingSerializer,
    TaskSerializer,
    RoutinePresetSerializer,
    AcademicEventSerializer,
    HabitCheckinSerializer,
    HabitSerializer,
)


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    @action(detail=True, methods=["GET"])
    def summary(self, request, pk=None):
        semester = self.get_object()
        total_courses = semester.courses.count()

        total_events = 0
        completed_events = 0

        for course in semester.courses.all():
            total_events += course.events.count()
            completed_events += course.events.filter(
                status="completed"
            ).count()

        completion_percentage = (
            (completed_events / total_events) * 100
            if total_events > 0
            else 0
        )

        return Response({
            "semester_name": semester.name,
            "total_courses": total_courses,
            "total_events": total_events,
            "completed_events": completed_events,
            "completion_percentage": round(
                completion_percentage, 2
            ),
        })


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

    @action(detail=False, methods=["GET"])
    def overdue(self, request):
        today = timezone.now().date()

        tasks = self.queryset.filter(
            due_at__lt=today
        ).exclude(status="completed")

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def today(self, request):
        today = timezone.now().date()

        tasks = self.queryset.filter(
            due_at__date=today
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @action(detail=True, methods=["GET"])
    def streak(self, request, pk=None):
        habit = self.get_object()

        current_streak = habit.get_current_streak()
        best_streak = habit.get_best_streak()

        return Response({
            "habit_name": habit.name,
            "current_streak": current_streak,
            "best_streak": best_streak,
        })


class HabitCheckinViewSet(viewsets.ModelViewSet):
    queryset = HabitCheckin.objects.all()
    serializer_class = HabitCheckinSerializer