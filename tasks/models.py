from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
import pytz
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Semester(models.Model):
    """Academic semester (Fall 2026, Spring 2027, etc.)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=100, help_text="e.g., Fall 2026")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.start_date.year})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date')


class Course(models.Model):
    """Course within a semester"""
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, help_text="e.g., CS101")
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color for UI")
    credits = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['semester', 'code']
    
    def __str__(self):
        return f"{self.code}: {self.name}"


# ===== CLASS MEETINGS =====

class ClassMeeting(models.Model):
    """When and where a class meets"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='meetings')
    days_of_week = models.CharField(
        max_length=20,
        help_text="e.g., '1,3,5' for Mon,Wed,Fri"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.start_time} to {self.end_time}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time')
    
    def get_days_list(self):
        """Convert days_of_week string like '1,3,5' into a
        list of integers [1, 3, 5] for easier checking"""
        return [int(d) for d in self.days_of_week.split(',') if d]


class RoutinePreset(models.Model):
    """Reusable day patterns like MW (Monday-Wednesday)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presets')
    name = models.CharField(max_length=50, help_text="e.g., MW, ST, MWF")
    days_of_week = models.CharField(max_length=20, help_text="e.g., '1,3'")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name}"
    
    def get_days_list(self):
        return [int(d) for d in self.days_of_week.split(',') if d]


# ===== ACADEMIC EVENTS =====

class AcademicEvent(models.Model):
    """Assignments, quizzes, exams, presentations"""
    EVENT_TYPES = [
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('presentation', 'Presentation'),
        ('project', 'Project'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_datetime']
    
    def __str__(self):
        return f"{self.title} ({self.course.code})"


# ===== TASKS =====

class Task(models.Model):
    """Personal tasks - normal or advanced (time-block)"""
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    REMINDER_CHOICES = [
        ('none', 'None'),
        ('notification', 'Notification'),
        ('alarm', 'Alarm'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    due_at = models.DateTimeField(blank=True, null=True, help_text="When task is due")
    is_advanced = models.BooleanField(default=False, help_text="Time-block task?")
    start_at = models.DateTimeField(blank=True, null=True, help_text="Start of time block")
    end_at = models.DateTimeField(blank=True, null=True, help_text="End of time block")
    reminder_type = models.CharField(max_length=20, choices=REMINDER_CHOICES, default='none')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-due_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_advanced:
            if not self.start_at or not self.end_at:
                raise ValidationError('Advanced tasks must have start and end times')
            if self.end_at <= self.start_at:
                raise ValidationError('End time must be after start time')


# ===== HABITS =====

class Habit(models.Model):
    """Daily habits to track"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_current_streak(self):
        """Calculate current streak (consecutive checked days) by counting backwards from today until a gap is found"""

        """Calculate current streak (consecutive checked days)"""
        today = timezone.now().date()
        streak = 0
        current_date = today
        
        while True:
            checkin = HabitCheckin.objects.filter(
                habit=self,
                date=current_date,
                checked=True
            ).first()
            
            if not checkin:
                break
            
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def get_best_streak(self):
        """Find best streak in history"""
        checkins = HabitCheckin.objects.filter(
            habit=self,
            checked=True
        ).order_by('date').values_list('date', flat=True)
        
        if not checkins:
            return 0
        
        best = 1
        current = 1
        dates_list = list(checkins)
        
        for i in range(1, len(dates_list)):
            if (dates_list[i] - dates_list[i-1]).days == 1:
                current += 1
                best = max(best, current)
            else:
                current = 1
        
        return best


class HabitCheckin(models.Model):
    """Daily checkin for a habit"""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='checkins')
    date = models.DateField()
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"