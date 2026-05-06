from django.db import models


class CompletedTaskManager(models.Manager):
    """Менеджер для получения только завершенных задач"""

    def get_queryset(self):
        return super().get_queryset().filter(status='completed')


class ActiveTaskManager(models.Manager):
    """Менеджер для получения активных задач (не завершенных)"""

    def get_queryset(self):
        return super().get_queryset().exclude(status='completed')