from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


# Trip Model
class Trip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    start_lat = models.FloatField()
    start_lng = models.FloatField()
    
    end_lat = models.FloatField(blank=True, null=True)
    end_lng = models.FloatField(blank=True, null=True)
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.start_time}"


# Stop Model (Multiple stops in a trip)
class Stop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stop at {self.latitude}, {self.longitude}"


# Visit Report Model
class VisitReport(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title