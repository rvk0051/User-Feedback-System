from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .forms.authentication import EmailAuthenticationForm
from .views import (
    register_view,
    dashboard_view,
    submit_feedback,
    feedback_list_view,
    export_feedback_csv,
    home_redirect_view
)
from .api_views import (
    FeedbackListCreateAPIView,
    FeedbackDetailAPIView,
    FeedbackUpdateAPIView,
)

from .forms.authentication import SimplePasswordChangeForm
from .views.auth_views import change_password_view

# Authentication URLs
auth_patterns = [
    path('login/', LoginView.as_view(
        authentication_form=EmailAuthenticationForm,
        template_name='authorization_and_authentication/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register_view, name='register'),
]

# Password management URLs
password_patterns = [
    path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            form_class=SimplePasswordChangeForm,
            template_name='feedback_system/password_change.html',
            success_url='/password/change/done/'
        ),
        name='password_change'
    ),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='authorization_and_authentication/password_change_done.html'
    ), name='password_change_done'),
]

# Feedback URLs
feedback_patterns = [
    path('feedback/submit/', submit_feedback, name='submit_feedback'),
    path('feedback/', feedback_list_view, name='feedback_list'),
    path('feedback/export-csv/', export_feedback_csv, name='export_feedback_csv'),

    path('api/feedback/', FeedbackListCreateAPIView.as_view(), name='api_feedback_list_create'),
    path('api/feedback/<int:pk>/', FeedbackDetailAPIView.as_view(), name='api_feedback_detail'),
    path('api/feedback/<int:pk>/update/', FeedbackUpdateAPIView.as_view(), name='api_feedback_update'),
]

# Main URL patterns
urlpatterns = [
    path('', home_redirect_view, name='home_redirect'),  # root URL
    path('dashboard/', dashboard_view, name='dashboard'),
    *auth_patterns,
    *password_patterns,
    *feedback_patterns,
]