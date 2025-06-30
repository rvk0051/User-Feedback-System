from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer

# View 1: List all feedbacks and allow new feedback submission
class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()  # fetch all feedbacks
    serializer_class = FeedbackSerializer  # use the serializer we just made
    permission_classes = [permissions.IsAuthenticated]  # user must be logged in

    # This method automatically assigns the logged-in user to the submitted feedback
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View 2: View details of one, for which authentication is needed.
class FeedbackDetailAPIView(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

# View 3: Staff can update feedback (e.g. mark as resolved)
class FeedbackUpdateAPIView(generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAdminUser]  # Only staff/admin allowed
