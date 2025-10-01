from django.contrib import admin
from .models import Issue, Comment, ReviewRequest

# Register your models here.

admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(ReviewRequest)