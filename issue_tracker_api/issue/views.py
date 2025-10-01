from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Issue,Comment, ReviewRequest
from .serializers import IssueSerializers, ReviewRequestSerializer, CommentSerializer
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

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        issue_id = self.request.query_params.get('issue')
        if issue_id:
            return Comment.objects.filter(issue_id=issue_id).order_by('-created_at')
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewRequestViewSet(viewsets.ModelViewSet):
    queryset = ReviewRequest.objects.all().order_by('-created_at')
    serializer_class = ReviewRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ReviewRequest.objects.all().order_by('-created_at')
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            return ReviewRequest.objects.none()
        return ReviewRequest.objects.filter(employee=employee).order_by('-created_at')

    def perform_create(self, serializer):
        """Auto-assign employee from request.user and set issue status to Review"""
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise ValueError("No Employee profile found for this user")

        issue = serializer.validated_data['issue']
        issue.status = "Review"   # ✅ set to Review instead of blocked
        issue.save()

        serializer.save(employee=employee)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def decide(self, request, pk=None):
        review = self.get_object()

        approved = request.data.get('approved', None)
        feedback = request.data.get('feedback', '')

        if approved is None:
            return Response({'detail': 'approved (true/false) is required'}, status=status.HTTP_400_BAD_REQUEST)

        review.reviewed = True
        review.approved = bool(approved)
        review.feedback = feedback

        issue = review.issue
        if review.approved:
            issue.status = "Resolved"
        else:
            issue.status = "In Progress"
            if feedback:
                try:
                    employee = Employee.objects.get(user=request.user)
                    Comment.objects.create(issue=issue, author=employee, text=f"Review feedback: {feedback}")
                except Employee.DoesNotExist:
                # fallback if admin has no Employee profile
                    pass

        issue.save()
        review.save()

        serializer = self.get_serializer(review)
        return Response(serializer.data)