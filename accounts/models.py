import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


'''
AUTH_USER_MODEL = 'accounts.User' add this to settings it comes with AbstractUser
'''

class User(AbstractUser):
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

    WEEKDAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='Asia/Dhaka'
    )

    week_start_day = models.CharField(
        max_length=10,
        choices=WEEKDAY_CHOICES,
        default='monday'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username