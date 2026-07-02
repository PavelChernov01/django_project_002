import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task, Project
from account.models import User

print("Создание тестовых данных...")

# Получаем пользователя и проект
user = User.objects.first()
if not user:
    user = User.objects.create(
        phone='+79991112233',
        email='test@example.com',
        first_name='Тест',
        last_name='Тестов'
    )
    user.set_password('123')
    user.save()
    print("Создан тестовый пользователь")

project = Project.objects.first()
if not project:
    project = Project.objects.create(name='Тестовый проект', owner=user)
    print("Создан тестовый проект")

# Создаём задачи с разными статусами
tasks_data = [
    {'title': 'Завершенная задача 1', 'status': 'completed'},
    {'title': 'Завершенная задача 2', 'status': 'completed'},
    {'title': 'Завершенная задача 3', 'status': 'completed'},
    {'title': 'Задача в работе', 'status': 'started'},
    {'title': 'Новая задача', 'status': 'created'},
    {'title': 'Отмененная задача', 'status': 'cancelled'},
]

for task_data in tasks_data:
    task, created = Task.objects.get_or_create(
        title=task_data['title'],
        project=project,
        defaults={
            'status': task_data['status'],
            'priority': 2
        }
    )
    if not created:
        task.status = task_data['status']
        task.save()
    task.users.add(user)
    print(f"{'Создана' if created else 'Обновлена'}: {task.title} (статус: {task.status})")

print("\nГотово!")
print(f"Всего задач: {Task.objects.count()}")
print(f"Завершенных задач: {Task.objects.filter(status='completed').count()}")