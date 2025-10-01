from rest_framework import serializers
from .models import Issue, Comment, ReviewRequest


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'text', 'created_at']


class ReviewRequestSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source="employee.user.username", read_only=True)
    issue_title = serializers.CharField(source="issue.title", read_only=True)

    class Meta:
        model = ReviewRequest
        fields = [
            'id',
            'issue',         # 🔑 write-only when creating
            'issue_title',   # human-readable
            'employee',      # username
            'created_at',
            'reviewed',
            'approved',
            'feedback',
        ]
        extra_kwargs = {
            'issue': {'write_only': True},  # ✅ allows POST with {"issue": id}
        }


class IssueSerializers(serializers.ModelSerializer):
    latest_feedback = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'  # includes all model fields + the custom ones
        extra_fields = ['latest_feedback', 'comments_count']

    def get_latest_feedback(self, obj):
        last = obj.review_requests.order_by('-created_at').first()
        return last.feedback if last and last.feedback else None

    def get_comments_count(self, obj):
        return obj.comments.count()
