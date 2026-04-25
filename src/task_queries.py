import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task

print("=" * 50)
print("ЗАДАНИЯ 6-10")
print("=" * 50)

# 6) Получить список задач, которые были переоткрыты
print("\n6) Переоткрытые задачи:")
tasks_reopened = Task.objects.filter(status='reopened')
for task in tasks_reopened:
    print("   ", task.title)

# 7) Отсортировать задачи по приоритету (убывание), затем по дате (сначала новые)
print("\n7) Задачи по приоритету и дате:")
tasks_sorted = Task.objects.order_by('-priority', '-created_at')
for task in tasks_sorted:
    print("   ", task.title, "- приоритет:", task.priority)

# 8) Подсчитать общее количество задач
print("\n8) Общее количество задач:", Task.objects.count())

# 9) Найти самую последнюю созданную задачу
print("\n9) Самая последняя задача:")
latest_task = Task.objects.order_by('-created_at').first()
print("   ", latest_task.title)

# 10) Получить все задачи в работе (без completed и cancelled)
print("\n10) Задачи в работе (без завершенных и отмененных):")
tasks_working = Task.objects.exclude(status='completed').exclude(status='cancelled')
for task in tasks_working:
    print("   ", task.title, "-", task.status)