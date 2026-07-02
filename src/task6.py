import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Project

# Получаем проекты с детальным описанием
projects = Project.objects.filter(details__isnull=False)

print("=" * 50)
print("Проекты с подробным описанием в ProjectDetails")
print("=" * 50)

for project in projects:
    print(f"\nНазвание: {project.name}")
    print(f"Владелец: {project.owner}")
    print(f"Бюджет: {project.details.budget}")
    print(f"Дедлайн: {project.details.deadline}")
    print(f"Репозиторий: {project.details.repository_url}")
    print("-" * 30)

print(f"\nИТОГО: {projects.count()} проектов с детальным описанием")