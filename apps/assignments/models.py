from django.db import models

from apps.base.models import BaseModel
from .constants import AssignmentStatus


class Assignments(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30, choices=AssignmentStatus.STATUS_CHOICES, default=AssignmentStatus.PENDING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'

    def __str__(self):
        return f"{self.user} - {self.title}"
