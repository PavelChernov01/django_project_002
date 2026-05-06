import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task, Comment
from account.models import User
from task_manager.models import Project

print("=" * 50)
print("ПРОВЕРКА ЗАДАЧИ №6")
print("=" * 50)

# Подготавливаем данные
project = Project.objects.first()
if not project:
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
    project = Project.objects.create(name='Проект для сигнала', owner=user)
    print("Создан проект")

user = User.objects.first()
print(f"Пользователь: {user.first_name} {user.last_name}")

# Создаем задачу
print("\nСоздание новой задачи...")
task = Task.objects.create(
    title='Тестовая задача для сигнала',
    project=project,
    status='created',
    priority=2
)
task.users.add(user)
print(f"Задача создана: {task.title}")

# Проверяем комментарии
comments = Comment.objects.filter(task=task)
print(f"\nКомментариев к задаче: {comments.count()}")

for comment in comments:
    print(f"  - {comment.text}")

if comments.count() > 0:
    print("\n✅ ЗАДАЧА №6 РЕШЕНА! Комментарий создан автоматически.")
else:
    print("\n❌ Ошибка: Комментарий не создан.")