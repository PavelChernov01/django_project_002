import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.models import Count
from account.models import User
from task_manager.models import Task

users = User.objects.annotate(comments_count=Count('comments')).filter(comments_count__gt=2)

for user in users:
    print("Пользователь:", user.phone, "- комментариев:", user.comments_count)
    tasks = Task.objects.filter(users=user)
    for task in tasks:
        print("  Задача:", task.title)
    print()