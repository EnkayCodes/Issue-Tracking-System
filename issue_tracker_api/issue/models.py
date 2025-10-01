from django.db import models
from employee.models import Employee

class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="issues")

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Review', 'Review'),        # ✅ renamed
        ('Resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    issue_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    
class Comment(models.Model):
    issue = models.ForeignKey('Issue', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Employee, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.issue.title}"

class ReviewRequest(models.Model):
    issue = models.ForeignKey('Issue', related_name='review_requests', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='review_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)          # whether admin processed it
    approved = models.BooleanField(null=True, blank=True)  # True=approved, False=rejected, null=pending
    feedback = models.TextField(blank=True, null=True)     # admin feedback when rejected

    def __str__(self):
        status = "Pending" if self.approved is None else ("Approved" if self.approved else "Rejected")
        return f"ReviewRequest({self.issue.title}) by {self.employee.username} - {status}"