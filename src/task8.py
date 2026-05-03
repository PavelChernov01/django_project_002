import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from task_manager.models import Task, Tag

print("=" * 50)
print("ЗАДАЧА №8: ЗАДАЧИ С ТЕГОМ 'DJANGO'")
print("=" * 50)

# 1. Создаём тег "Django"
tag, created = Tag.objects.get_or_create(name='Django')

if created:
    print("Создан тег: Django")
else:
    print("Тег Django уже существует")

# 2. Добавляем тег "Django" ко всем задачам (или к первым 8)
tasks_all = Task.objects.all()

if tasks_all.count() > 0:
    for task in tasks_all:
        task.tags.add(tag)
    print("Тег Django добавлен ко всем", tasks_all.count(), "задачам")
else:
    print("Нет задач в базе данных")
    print("Сначала создайте задачи через задачу №4")

print()

# 3. Получаем задачи с тегом "Django"
tasks_with_tag = Task.objects.filter(tags=tag)

print("Результат:")
print("-" * 50)
print("Найдено задач с тегом 'Django':", tasks_with_tag.count())
print("-" * 50)

if tasks_with_tag.count() > 0:
    for task in tasks_with_tag:
        print("Задача:", task.title)
        print("Проект:", task.project.name)
        print()
    print("=" * 50)
    print("ЗАДАЧА №8 РЕШЕНА")
    print("=" * 50)
else:
    print("Задачи с тегом 'Django' не найдены")