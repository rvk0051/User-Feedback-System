from django import forms
from django.contrib.auth.forms import SetPasswordForm

class SimplePasswordChangeForm(SetPasswordForm):
    # This form only keeps the new password and confirmation fields
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )