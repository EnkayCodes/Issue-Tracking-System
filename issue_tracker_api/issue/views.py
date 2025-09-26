from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializers
from employee.models import Employee

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializers
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_issues(self, request):
        try:
            # ✅ Get the Employee linked to the logged-in user
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found"}, status=404)

        # ✅ Filter issues for this employee
        issues = Issue.objects.filter(assigned_to=employee)
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)
