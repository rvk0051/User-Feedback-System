from django.contrib import messages  # To show success/error messages
from ..forms import SimplePasswordChangeForm  # Add this import
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from ..forms.registration import RegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('feedback_list')  # Redirect to feedback listing
    else:
        form = RegistrationForm()

    return render(request, 'authorization_and_authentication/register.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = SimplePasswordChangeForm(user=request.user, data=request.POST)  # Use SimplePasswordChangeForm
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was changed successfully!")
            return redirect('dashboard')
    else:
        form = SimplePasswordChangeForm(user=request.user)  # Use SimplePasswordChangeForm

    return render(request, 'feedback_system/password_change.html', {'form': form})