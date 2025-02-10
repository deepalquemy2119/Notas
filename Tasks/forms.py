from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'important': 'Mark as Important',
        }
        error_messages = {
            'title': {'required': 'Please enter a task title.'},
            'description': {'required': 'Please enter a task description.'},
        }