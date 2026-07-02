from django.db import models


class BaseModel(models.Model):
    """Абстрактная базовая модель с общими полями"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        abstract = True  # Это абстрактная модель - таблица в БД не создаётся

    def __str__(self):
        return f'{self.__class__.__name__} #{self.pk}'