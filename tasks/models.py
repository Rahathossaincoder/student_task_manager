from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.










class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Semester(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)


class ClassMeeting:
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=20)
    start_date = models.TimeField()
    end_date = models.TimeField()
    room_location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date can not be after end date.")




class RoutinePreset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=100, unique=True)
    days = models.CharField(max_length=20)
    start_date = models.TimeField()
    end_date = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class AcademicEvent(models.Model):
    status_choise = (
        ("PENDING" , "Pending")
        ("IN_PROGRESS" , "in_progress"),
        ("COMPLETED" , "completed")
    )

    '''
        # Django automatically adds this validation:
    def clean_month(self):
        month = self.cleaned_data['month']
        valid_choices = ['JANUARY', 'FEBRUARY']  # The keys from MONTH_CHOICES
        if month not in valid_choices:
            raise ValidationError('Invalid month choice')
        return month
        '''
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=status_choise)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    status = (
        ("PENDING" , "Pending")
        ("IN_PROGRESS" , "in_progress"),
        ("COMPLETED" , "completed")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_advanced = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

'''
Habit
id → AutoField (primary key)
user → ForeignKey (to User, on_delete=CASCADE)
name → CharField (max_length=100)
active → BooleanField (default=True)
created_at → DateTimeField (auto_now_add=True)

'''
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    '''
HabitCheckin
id → AutoField (primary key)
habit → ForeignKey (to Habit, on_delete=CASCADE)
date → DateField
checked → BooleanField (default=False)
created_at → DateTimeField (auto_now_add=True)
Unique constraint: (habit, date)'''

class HabitCheckin(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, unique=True)
    date = models.DateField(unique=True)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)







