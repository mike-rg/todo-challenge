from django.db import models

from apps.base.models import BaseModel
from .constants import AssignmentStatus


class Assignment(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30, choices=AssignmentStatus.STATUS_CHOICES, default=AssignmentStatus.PENDING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.title}"
