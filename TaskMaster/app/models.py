from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def is_expired(self):
        return self.due_date < datetime.now() if self.due_date else False

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
