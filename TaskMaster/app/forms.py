from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'due_date']
