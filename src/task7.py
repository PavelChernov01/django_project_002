import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task

# Получаем все задачи проекта с ID=3
tasks = Task.objects.filter(project_id=3)

print("=" * 50)
print("ЗАДАЧИ ПРОЕКТА ID=3")
print("=" * 50)
print(f"Всего задач: {tasks.count()}\n")

for task in tasks:
    print(f"- {task.title}")