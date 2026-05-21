from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SemesterViewSet,CourseViewSet,ClassMeetingViewSet,RoutinePresetViewSet,
    AcademicEventViewSet,TaskViewSet,HabitViewSet,HabitCheckinViewSet
)

router = DefaultRouter()
router.register('semester', SemesterViewSet)
router.register('courses', CourseViewSet)
router.register('class_meeting', ClassMeetingViewSet)
router.register('routine_preset', RoutinePresetViewSet)
router.register('academic_event', AcademicEventViewSet)
router.register('task_view', TaskViewSet)
router.register('habit_view', HabitViewSet)
router.register('habit_checkin', HabitCheckinViewSet)


urlpatterns = [
    path('', include(router.urls)),
]