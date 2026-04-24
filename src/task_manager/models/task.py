from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
        ('reopened', 'Переоткрыта'),
    ]

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    priority = models.IntegerField()

    def __str__(self):
        return self.title