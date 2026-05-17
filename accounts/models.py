from django.db import models

# Create your models here.

'''
User
id (primary key, auto)
username
email
password
first_name
last_name
created_at

'''

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=300, unique=True)
    password = models.CharField (max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.CharField(auto_now_add = True)
