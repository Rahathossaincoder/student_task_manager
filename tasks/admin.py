
from django.contrib import admin
from tasks.models import (
    Semester, Course, ClassMeeting, RoutinePreset,
    AcademicEvent, Task, Habit, HabitCheckin
)

# Register each model
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(ClassMeeting)
admin.site.register(RoutinePreset)
admin.site.register(AcademicEvent)
admin.site.register(Task)
admin.site.register(Habit)
admin.site.register(HabitCheckin)