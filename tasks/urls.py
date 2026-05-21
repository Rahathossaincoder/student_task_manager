from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SemesterViewSet,CourseViewSet,ClassMeetingViewSet,RoutinePresetViewSet,
    AcademicEventViewSet,TaskViewSet,HabitViewSet,HabitCheckinViewSet
)

router = DefaultRouter()
router.register('drinks', SemesterViewSet)
router.register('drinks', CourseViewSet)
router.register('drinks', ClassMeetingViewSet)
router.register('drinks', RoutinePresetViewSet)
router.register('drinks', AcademicEventViewSet)
router.register('drinks', TaskViewSet)
router.register('drinks', HabitViewSet)
router.register('drinks', HabitCheckinViewSet)


urlpatterns = [
    path('', include(router.urls)),
]