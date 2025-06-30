from django.urls import path
from .api_views import FeedbackListCreateAPIView, FeedbackDetailAPIView

urlpatterns = [
    # List all feedbacks or submit new feedback
    path('feedback/', FeedbackListCreateAPIView.as_view(), name='api_feedback_list_create'),

    # Retrieve, update, or delete a single feedback by its ID
    path('feedback/<int:pk>/', FeedbackDetailAPIView.as_view(), name='api_feedback_detail'),
]
