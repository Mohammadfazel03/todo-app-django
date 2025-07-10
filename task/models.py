from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
