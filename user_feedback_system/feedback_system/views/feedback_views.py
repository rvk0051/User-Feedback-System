# feedback_views.py
from django.http import HttpResponse
import csv
from ..forms.feedback import FeedbackForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ..models import Feedback
from django.db.models import Q

@login_required
def feedback_list_view(request):
    user = request.user

    # Base queryset
    if user.is_staff:
        feedbacks = Feedback.objects.all()
    else:
        feedbacks = Feedback.objects.filter(user=user)

    # Search filter
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', '-created_at')

    if search:
        feedbacks = feedbacks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if status:
        feedbacks = feedbacks.filter(status=status)

    # Sorting
    feedbacks = feedbacks.order_by(sort)

    # Pagination
    paginator = Paginator(feedbacks, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate visible page range
    if paginator.num_pages <= 5:
        page_range = paginator.page_range
    else:
        if page_obj.number <= 3:
            page_range = range(1, 6)
        elif page_obj.number >= paginator.num_pages - 2:
            page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            page_range = range(page_obj.number - 2, page_obj.number + 3)

    context = {
        'feedbacks': page_obj,
        'search': search,
        'status': status,
        'sort': sort,
        'is_paginated': page_obj.has_other_pages(),
        'page_range': page_range,
    }
    return render(request, 'feedback_system/feedback_list.html', context)

# Submit feedback (only for authenticated users)
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Don't save to DB yet
            feedback.user = request.user       # Assign the current logged-in user
            feedback.save()                    # Now save to DB with user

            # Email code (if added)
            # send_mail(...)

            return redirect('feedback_list')
    else:
        form = FeedbackForm()

    return render(request, 'feedback_system/feedback_form.html', {'form': form})

@login_required
def export_feedback_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Status', 'Created At', 'User'])

    # If staff user, export all feedbacks
    if request.user.is_staff:
        feedbacks = Feedback.objects.all()
    else:
        # For regular users, export only their feedbacks
        feedbacks = Feedback.objects.filter(user=request.user)

    for feedback in feedbacks:
        writer.writerow([
            feedback.title,
            feedback.description,
            feedback.status,
            feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            feedback.user.email
        ])

    return response