from django.contrib import admin

# Register your models here.


from tasks.models import (
    User
)

# Register each model
admin.site.register(User)