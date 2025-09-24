from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    position = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
