import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.models import Prefetch
from task_manager.models import Task, Comment

print("=" * 60)
print("ЗАДАЧА №3: СПИСОК ЗАДАЧ С КОММЕНТАРИЯМИ")
print("=" * 60)

# Способ 1: Обычный prefetch_related
tasks = Task.objects.prefetch_related('comments')

for task in tasks:
    print(f"\nЗадача: {task.title}")
    print(f"Проект: {task.project.name}")

    comments = task.comments.all()
    print(f"Комментариев: {comments.count()}")

    if comments.count() > 0:
        print("Комментарии:")
        for comment in comments:
            print(f"  - Автор: {comment.author.first_name} {comment.author.last_name}")
            print(f"    Текст: {comment.text[:80]}")
            print(f"    Дата: {comment.created_at.strftime('%d.%m.%Y %H:%M')}")
    else:
        print("  Комментариев нет")
    print("-" * 40)