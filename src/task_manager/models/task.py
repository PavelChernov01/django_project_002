from django.db import models
from account.models import User
from .project import Project
from .tag import Tag
from ..managers import CompletedTaskManager, ActiveTaskManager  # Добавьте эту строку


class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('reopened', 'Reopened'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    users = models.ManyToManyField(
        User,
        related_name='tasks'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tasks',
        blank=True
    )

    # Стандартный менеджер
    objects = models.Manager()

    # Кастомные менеджеры
    completed = CompletedTaskManager()
    active = ActiveTaskManager()

    class Meta:
        ordering = ['-priority', '-created_at']
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title