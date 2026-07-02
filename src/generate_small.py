import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from account.models import User
from task_manager.models import Project, Task, Comment, Tag

fake = Faker('ru_RU')

print("Генерация данных (упрощённая версия)...")

# 1. Очищаем старые теги и создаём новые
print("\n1. Создание тегов...")

# Удаляем все существующие теги
Tag.objects.all().delete()
print("   Старые теги удалены")

tag_names = ['bug', 'feature', 'urgent', 'test', 'deploy']
tags = []

for name in tag_names:
    tag = Tag(name=name)
    tag.save()
    tags.append(tag)
    print(f"   Создан тег: {name}")

print(f"   Всего тегов: {len(tags)}")

# 2. Пользователи
print("\n2. Создание пользователей...")
users = []
for i in range(10):
    user = User(
        phone=fake.unique.phone_number(),
        email=fake.unique.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    user.set_password('123')
    user.save()
    users.append(user)
print(f"   Создано пользователей: {len(users)}")

# 3. Проекты
print("\n3. Создание проектов...")
projects = []
for i in range(5):
    project = Project.objects.create(
        name=fake.company(),
        owner=random.choice(users)
    )
    projects.append(project)
print(f"   Создано проектов: {len(projects)}")

# 4. Задачи
print("\n4. Создание задач...")
statuses = ['created', 'started', 'completed', 'cancelled']
priorities = [1, 2, 3, 4]

for i in range(100):
    task = Task(
        title=fake.sentence(nb_words=5)[:100],
        status=random.choice(statuses),
        priority=random.choice(priorities),
        project=random.choice(projects)
    )
    task.save()

    responsible = random.sample(users, k=random.randint(1, 2))
    task.users.set(responsible)
    task.tags.set(random.sample(tags, k=random.randint(0, 2)))

    if (i + 1) % 20 == 0:
        print(f"   Создано задач: {i + 1}")

print(f"   Всего задач: {Task.objects.count()}")

# 5. Комментарии
print("\n5. Создание комментариев...")
comments_count = 0
for task in Task.objects.all()[:50]:
    for _ in range(random.randint(0, 3)):
        Comment.objects.create(
            text=fake.sentence(),
            task=task,
            author=random.choice(users)
        )
        comments_count += 1

print(f"   Создано комментариев: {comments_count}")

# Итог
print("\n" + "=" * 40)
print("ГЕНЕРАЦИЯ ЗАВЕРШЕНА!")
print("=" * 40)
print(f"Пользователей: {User.objects.count()}")
print(f"Проектов: {Project.objects.count()}")
print(f"Задач: {Task.objects.count()}")
print(f"Комментариев: {Comment.objects.count()}")
print(f"Тегов: {Tag.objects.count()}")
print("=" * 40)