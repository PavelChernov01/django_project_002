import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task

# Получаем задачи с комментариями
tasks = Task.objects.filter(comments__isnull=False).distinct()

print("Задачи у которых есть комментарии:")
print("-" * 40)

for task in tasks:
    count = task.comments.count()
    print(f"Задача: {task.title}")
    print(f"Проект: {task.project.name}")
    print(f"Комментариев: {count}")
    print("-" * 40)

print(f"ИТОГО: {tasks.count()} задач")