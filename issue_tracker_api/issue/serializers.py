from rest_framework import serializers
from .models import Issue

class IssueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
