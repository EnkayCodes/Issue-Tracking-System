from django.db import models
from employee.models import Employee

# Create your models here.
class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="issues")
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('blocked', 'blocked'),
        ('Resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Meduim', 'Meduim'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    issue_deadline = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.title}"