from django_filters import rest_framework as filters
from django_filters import DateTimeFilter, CharFilter, NumberFilter
from .models import Task
from account.models import User


# ============================================
# ЗАДАЧА 4: Фильтр по диапазону дат
# ============================================
class TaskDateFilter(filters.FilterSet):
    """Фильтр задач по диапазону дат"""
    created_at__gte = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['created_at__gte', 'created_at__lte']


# ============================================
# ЗАДАЧА 5: Полный FilterSet для задач
# ============================================
class TaskFilter(filters.FilterSet):
    """Фильтр для модели Task"""
    # Фильтр по статусу
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)

    # Фильтр по приоритету
    priority = filters.NumberFilter(field_name='priority', lookup_expr='exact')

    # Диапазон дат
    created_at__gte = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = DateTimeFilter(field_name='created_at', lookup_expr='lte')

    # Поиск по описанию
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'created_at__gte', 'created_at__lte', 'description']


# ============================================
# ЗАДАЧА 3: Фильтр пользователя (видит только свои задачи)
# ============================================
class UserTaskFilter(filters.FilterSet):
    """Фильтр для задач пользователя"""

    class Meta:
        model = Task
        fields = ['status', 'priority']