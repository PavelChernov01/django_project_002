from django.db import models
from .person import Person


class Employee(Person):
    """Модель сотрудника - наследуется от Person"""
    employee_id = models.CharField('Табельный номер', max_length=20, unique=True)
    position = models.CharField('Должность', max_length=100)
    hire_date = models.DateField('Дата приёма на работу')
    salary = models.DecimalField('Зарплата', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.position})'