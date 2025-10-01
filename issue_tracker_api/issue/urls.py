from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueViewSet, CommentViewSet, ReviewRequestViewSet

router = DefaultRouter()
router.register(r'issue', IssueViewSet, basename='issue')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'review-requests', ReviewRequestViewSet, basename='review-requests')


urlpatterns = [
    path('', include(router.urls)),
]
