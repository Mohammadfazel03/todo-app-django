from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task.models import Task


class CreateTaskForm(ModelForm):
    """Form for creating new tasks"""

    class Meta:
        model = Task
        fields = [
            "content"
        ]
