from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Feedback  # update this if your model path is different

@login_required
def dashboard_view(request):
    user = request.user

    # Get all feedbacks of this user
    user_feedbacks = Feedback.objects.filter(user=user)

    # Calculate statistics
    total = user_feedbacks.count()
    pending = user_feedbacks.filter(status='Pending').count()
    reviewed = user_feedbacks.filter(status='Reviewed').count()
    resolved = user_feedbacks.filter(status='Resolved').count()

    context = {
        'total_feedbacks': total,
        'pending_feedbacks': pending,
        'reviewed_feedbacks': reviewed,
        'resolved_feedbacks': resolved,
    }
    return render(request, 'feedback_system/dashboard.html', context)