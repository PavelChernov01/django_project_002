import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Comment, Task, Tag
from account.models import User

# 1. Получаем или создаём пользователя с ID=2
try:
    user = User.objects.get(id=2)
    print("Найден пользователь с ID=2:", user.phone)
except User.DoesNotExist:
    # Используем уникальный email
    import time
    unique_email = f'user2_{int(time.time())}@example.com'
    user = User(id=2, phone='+79999999999', email=unique_email)
    user.set_password('123')
    user.save()
    print("Создан пользователь с ID=2, email:", unique_email)

# 2. Получаем или создаём тег Django
tag, created = Tag.objects.get_or_create(name='Django')
print("Тег Django:", "создан" if created else "уже существует")

# 3. Добавляем тег Django к задачам
tasks = Task.objects.all()[:5]
for task in tasks:
    task.tags.add(tag)
print("Тег Django добавлен к", len(tasks), "задачам")

# 4. Создаём комментарии от пользователя
for task in tasks:
    comment, created = Comment.objects.get_or_create(
        task=task,
        author=user,
        defaults={'text': 'Комментарий от пользователя ID=2 к задаче с тегом Django'}
    )
    if created:
        print("Добавлен комментарий к задаче:", task.title[:30])

print()

# 5. Получаем комментарии пользователя ID=2 по задачам с тегом Django
tag = Tag.objects.get(name='Django')
tasks_with_django = Task.objects.filter(tags=tag)
comments = Comment.objects.filter(author=user, task__in=tasks_with_django)

print("=" * 50)
print("ЗАДАЧА №9")
print("=" * 50)
print("Пользователь ID:", user.id)
print("Тег: Django")
print("Найдено комментариев:", comments.count())
print("-" * 50)

for comment in comments:
    print("Комментарий:", comment.text)
    print("К задаче:", comment.task.title)
    print()

if comments.count() > 0:
    print("=" * 50)
    print("ЗАДАЧА №9 РЕШЕНА")
    print("=" * 50)
else:
    print("Комментарии не найдены")