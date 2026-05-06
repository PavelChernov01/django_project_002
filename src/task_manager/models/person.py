from django.db import models
from .base_model import BaseModel


class Person(BaseModel):
    """Модель человека - наследуется от BaseModel"""
    phone = models.CharField('Телефон', max_length=20, unique=True)
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=64)
    last_name = models.CharField('Фамилия', max_length=64)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    class Meta:
        db_table = 'persons'
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'