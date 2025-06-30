from django import forms
from ..models import Feedback

# Feedback submission form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter feedback title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your feedback'}),
        }