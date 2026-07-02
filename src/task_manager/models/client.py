from django.db import models
from .person import Person


class Client(Person):
    """Модель клиента - наследуется от Person"""
    client_id = models.CharField('ID клиента', max_length=20, unique=True)
    discount = models.DecimalField('Скидка', max_digits=5, decimal_places=2, default=0)
    total_purchases = models.DecimalField('Общая сумма покупок', max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name} (Клиент)'