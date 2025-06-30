from django.db import models
from django.conf import settings

class Feedback(models.Model):
    # Define possible status states for tracking feedback progress
    STATUS_CHOICES = [
        ('Pending', 'Pending'),     # Initial state when feedback is first submitted
        ('Reviewed', 'Reviewed'),   # Feedback has been looked at by staff
        ('Resolved', 'Resolved'),   # Final state when action has been taken
    ]

    # Basic information about the feedback
    title = models.CharField(max_length=255)

    # Detailed feedback content
    description = models.TextField()

    # Automatically set when feedback is created
    created_at = models.DateTimeField(
        auto_now_add=True  # Automatically set the field to now when object is created
    )

    # Link to the user who submitted the feedback
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use the project's custom user model
        on_delete=models.CASCADE   # Delete feedback if user is deleted
    )

    # Track the current state of the feedback
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,  # Limit status to predefined choices
        default='Pending'        # New feedback starts as pending
    )

    def __str__(self):
        """Provide a readable string representation of the feedback"""
        return f"{self.title} - {self.user.email}"