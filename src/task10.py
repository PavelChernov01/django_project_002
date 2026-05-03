import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Project, Task

# Получаем проекты, в которых есть задачи со статусом 'cancelled'
projects = Project.objects.filter(tasks__status='cancelled').distinct()

print("=" * 50)
print("ЗАДАЧА №10: ПРОЕКТЫ С ЗАДАЧАМИ СО СТАТУСОМ 'CANCELLED'")
print("=" * 50)
print("Найдено проектов:", projects.count())
print("-" * 50)

for project in projects:
    # Считаем сколько отмененных задач в проекте
    cancelled_count = Task.objects.filter(project=project, status='cancelled').count()
    print("Проект:", project.name)
    print("Отмененных задач:", cancelled_count)
    print()

if projects.count() > 0:
    print("=" * 50)
    print("ЗАДАЧА №10 РЕШЕНА")
    print("=" * 50)
else:
    print("Нет проектов с отмененными задачами")