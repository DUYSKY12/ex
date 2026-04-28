from django.db import models

class Staff(models.Model):
    fullname = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, unique=True) # e.g. EMP001
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='staff') # staff/manager
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} ({self.employee_id})"

class ActionLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    action = models.CharField(max_length=255) # e.g. "Updated Laptop ID: 4"
    timestamp = models.DateTimeField(auto_now_add=True)
