import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task, TaskHistory

# Очищаем старые данные
Task.objects.all().delete()

# Создаем задачи
tasks_data = [
    {"title": "Исправить ошибку входа", "status": "started", "priority": 5},
    {"title": "Создать меню", "status": "completed", "priority": 4},
    {"title": "Написать тесты", "status": "created", "priority": 5},
    {"title": "Обновить документацию", "status": "reopened", "priority": 2},
    {"title": "Развернуть проект", "status": "started", "priority": 5},
    {"title": "Оптимизировать БД", "status": "created", "priority": 4},
    {"title": "Добавить поиск", "status": "started", "priority": 3},
    {"title": "Настроить админку", "status": "completed", "priority": 3},
    {"title": "Сделать бэкап", "status": "reopened", "priority": 2},
    {"title": "Обновить библиотеки", "status": "cancelled", "priority": 1},
    {"title": "Исправить верстку", "status": "reopened", "priority": 4},
    {"title": "Написать документацию", "status": "created", "priority": 2},
]

for task_data in tasks_data:
    task = Task.objects.create(
        title=task_data["title"],
        status=task_data["status"],
        priority=task_data["priority"]
    )

    # Добавляем запись в историю
    TaskHistory.objects.create(
        task=task,
        changed_to=task_data["status"],
        change_reason="Создание задачи"
    )

print("Создано задач:", Task.objects.count())
print("Создано записей истории:", TaskHistory.objects.count())