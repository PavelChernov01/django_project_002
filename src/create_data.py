import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from account.models import User
from task_manager.models import Project, ProjectDetail, Task, Comment, Attachment, Tag

# Очистка всех данных
print("Очистка существующих данных...")
User.objects.all().delete()
Project.objects.all().delete()
ProjectDetail.objects.all().delete()
Tag.objects.all().delete()
Task.objects.all().delete()
Comment.objects.all().delete()
Attachment.objects.all().delete()
print("Готово!\n")

# Создание пользователей
print("1. Создание пользователей (8 шт)...")
users = []
phones = ['+79123456789', '+79223456789', '+79323456789', '+79423456789',
          '+79523456789', '+79623456789', '+79723456789', '+79823456789']
names = [('Иван', 'Иванов'), ('Петр', 'Петров'), ('Сидор', 'Сидоров'),
         ('Анна', 'Смирнова'), ('Елена', 'Кузнецова'), ('Михаил', 'Михайлов'),
         ('Ольга', 'Орлова'), ('Дмитрий', 'Дмитриев')]

for i, (phone, (first, last)) in enumerate(zip(phones, names)):
    user = User(phone=phone, first_name=first, last_name=last, email=f'user{i+1}@example.com')
    user.set_password('password123')
    user.save()
    users.append(user)
print("  Пользователи созданы!")

# Создание проектов
print("\n2. Создание проектов (8 шт)...")
projects = []
project_names = ['E-commerce Platform', 'Mobile App Development', 'CRM System', 'ERP Integration',
                'Data Analytics Dashboard', 'Cloud Migration', 'Security Audit', 'AI Chatbot']

for i, name in enumerate(project_names):
    project = Project.objects.create(name=name, owner=users[i % len(users)])
    projects.append(project)
print("  Проекты созданы!")

# Создание деталей проектов
print("\n3. Создание деталей проектов (8 шт)...")
budgets = [150000, 250000, 350000, 450000, 550000, 650000, 750000, 850000]
deadlines = ['2026-12-31', '2026-11-30', '2026-10-31', '2026-09-30',
             '2026-08-31', '2026-07-31', '2026-06-30', '2026-05-31']
repos = ['https://github.com/company/ecommerce', 'https://github.com/company/mobile-app',
         'https://github.com/company/crm', 'https://github.com/company/erp',
         'https://github.com/company/analytics', 'https://github.com/company/cloud',
         'https://github.com/company/security', 'https://github.com/company/chatbot']

for i, project in enumerate(projects):
    ProjectDetail.objects.create(project=project, budget=budgets[i], deadline=deadlines[i], repository_url=repos[i])
print("  Детали проектов созданы!")

# Создание тегов
print("\n4. Создание тегов (8 шт)...")
tag_names = ['Urgent', 'Important', 'Backend', 'Frontend', 'Bug', 'Feature', 'Documentation', 'Testing']
tags = []
for name in tag_names:
    tag = Tag.objects.create(name=name)
    tags.append(tag)
print("  Теги созданы!")

# Создание задач
print("\n5. Создание задач (8 проектов x 8 задач = 64 задачи)...")
task_statuses = ['created', 'started', 'completed', 'cancelled', 'reopened']
priorities = [1, 2, 3, 4]
task_titles = ['Setup', 'Design DB', 'Implement API', 'Create UI', 'Unit tests', 'Deploy', 'Optimization', 'Security']
tasks = []

for project in projects:
    for i, title in enumerate(task_titles):
        status = task_statuses[i % len(task_statuses)]
        priority = priorities[i % len(priorities)]
        task = Task.objects.create(
            title=f'{title} - {project.name}',
            description=f'Description for {title}',
            project=project,
            status=status,
            priority=priority
        )
        task.users.set(users[:min((i % 4) + 2, len(users))])
        task.tags.set(tags[i:min(i + 3, len(tags))])
        tasks.append(task)
print(f"  Задачи созданы! Всего: {len(tasks)}")

# Создание комментариев
print("\n6. Создание комментариев (8 задач x 8 комментариев = 64 комментария)...")
comment_texts = ['Great!', 'Need fix', 'Discuss', 'Done', 'Review PR', 'Blocker', 'Will do', 'Feedback']
for i, task in enumerate(tasks[:8]):
    for j, text in enumerate(comment_texts):
        Comment.objects.create(text=f'{text} - {task.title}', task=task, author=users[j % len(users)])
print("  Комментарии созданы!")

# Создание вложений
print("\n7. Создание вложений (8 задач x 8 файлов = 64 вложения)...")
file_names = ['spec.pdf', 'design.fig', 'api.md', 'report.xlsx', 'screenshot.png', 'config.yaml', 'req.txt', 'diagram.jpg']
for i, task in enumerate(tasks[:8]):
    for j, filename in enumerate(file_names):
        Attachment.objects.create(filename=f'task_{task.id}_{filename}', file=f'uploads/{filename}', task=task)
print("  Вложения созданы!")

# Статистика
print("\n" + "="*50)
print("=== СТАТИСТИКА ===")
print(f"Пользователей: {User.objects.count()}")
print(f"Проектов: {Project.objects.count()}")
print(f"Деталей проектов: {ProjectDetail.objects.count()}")
print(f"Тегов: {Tag.objects.count()}")
print(f"Задач: {Task.objects.count()}")
print(f"Комментариев: {Comment.objects.count()}")
print(f"Вложений: {Attachment.objects.count()}")
print("="*50)
print("\n🎉 ГОТОВО! 8 объектов каждой модели создано!")