from django.db import models
from .task import Task


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    changed_from = models.CharField(max_length=50, blank=True, null=True)
    changed_to = models.CharField(max_length=50)
    change_reason = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.changed_to}"