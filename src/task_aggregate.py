import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db.models import Count, Sum, Avg, Max, Min, Q, F
from django.db import connection
from task_manager.models import Task, Comment, Tag
from account.models import User

print("=" * 60)
print("ЗАДАЧИ ПО АГРЕГАЦИИ (1-10)")
print("=" * 60)

# ============================================
# 1.
# ============================================
print("\n1. Количество задач по каждому статусу:")
tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))
for item in tasks_by_status:
    print(f"   {item['status']}: {item['count']} задач")

# ============================================
# 2.
# ============================================
print("\n2. Пользователь с наибольшим количеством задач:")
user_with_most_tasks = User.objects.annotate(
    task_count=Count('tasks')
).order_by('-task_count').first()

if user_with_most_tasks:
    print(f"   Пользователь: {user_with_most_tasks.first_name} {user_with_most_tasks.last_name}")
    print(f"   Количество задач: {user_with_most_tasks.task_count}")

# ============================================
# 3.
# ============================================
print("\n3. Список задач с количеством комментариев:")
tasks_with_comments = Task.objects.annotate(
    comment_count=Count('comments')
).values('id', 'title', 'comment_count')[:10]

for task in tasks_with_comments:
    title = task['title'][:35] if len(task['title']) > 35 else task['title']
    print(f"   Задача {task['id']}: '{title}...' - комментариев: {task['comment_count']}")

# ============================================
# 4.
# ============================================
print("\n4. Задачи с более чем 3 комментариями:")
tasks_more_3_comments = Task.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count__gt=3)

for task in tasks_more_3_comments[:5]:
    title = task.title[:40] if len(task.title) > 40 else task.title
    print(f"   ID: {task.id} - {title}... - комментариев: {task.comments.count()}")

# ============================================
# 5.
# ============================================
print("\n5. Средний приоритет задач для каждого пользователя:")
users_avg_priority = User.objects.annotate(
    avg_priority=Avg('tasks__priority')
).exclude(avg_priority__isnull=True)

for user in users_avg_priority[:5]:
    name = f"{user.first_name} {user.last_name}".strip()
    if name == "":
        name = user.phone
    print(f"   {name}: средний приоритет = {user.avg_priority:.2f}")

# ============================================
# 6.
# ============================================
print("\n6. Сумма приоритетов задач по каждому тегу:")
tags_priority_sum = Tag.objects.annotate(
    total_priority=Sum('tasks__priority')
)

for tag in tags_priority_sum[:5]:
    total = tag.total_priority if tag.total_priority else 0
    print(f"   Тег '{tag.name}': сумма приоритетов = {total}")

# ============================================
# 7.
# ============================================
print("\n7. Задачи с комментариями больше, чем тегов:")
tasks_comments_vs_tags = Task.objects.annotate(
    comment_count=Count('comments'),
    tag_count=Count('tags')
).filter(comment_count__gt=F('tag_count'))

for task in tasks_comments_vs_tags[:5]:
    title = task.title[:35] if len(task.title) > 35 else task.title
    c_count = task.comments.count()
    t_count = task.tags.count()
    print(f"   {title}... - комментов: {c_count}, тегов: {t_count}")

# ============================================
# 8.
# ============================================
print("\n8. Топ-3 пользователя по комментариям в их задачах:")
users_by_comments = User.objects.annotate(
    total_comments=Count('tasks__comments')
).order_by('-total_comments')[:3]

for user in users_by_comments:
    name = f"{user.first_name} {user.last_name}".strip()
    if name == "":
        name = user.phone
    print(f"   {name}: {user.total_comments} комментариев в задачах")

# ============================================
# 9.
# ============================================
print("\n9. Raw SQL запрос: задачи с максимальным количеством комментариев:")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT t.id, t.title, COUNT(c.id) as comment_count
        FROM tasks t
        LEFT JOIN comments c ON t.id = c.task_id
        GROUP BY t.id, t.title
        ORDER BY comment_count DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    for row in rows:
        title = row[1][:35] if len(row[1]) > 35 else row[1]
        print(f"   Задача {row[0]}: '{title}...' - комментариев: {row[2]}")

# ============================================
# 10.
# ============================================
print("\n10. Задачи с комментариями > 5 и приоритетом выше среднего:")

avg_priority = Task.objects.aggregate(avg_priority=Avg('priority'))['avg_priority']
print(f"   Средний приоритет всех задач: {avg_priority:.2f}")

tasks_filtered = Task.objects.annotate(
    comment_count=Count('comments')
).filter(
    comment_count__gt=5,
    priority__gt=avg_priority
)

for task in tasks_filtered[:5]:
    title = task.title[:40] if len(task.title) > 40 else task.title
    print(f"   Задача: {title}...")
    print(f"      Комментариев: {task.comments.count()}, Приоритет: {task.priority} (средний: {avg_priority:.2f})")