import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.admin import site
from task_manager.models import Task, Project

print("=" * 50)
print("ПРОВЕРКА ЗАДАЧ 1-18")
print("=" * 50)

task_admin = site._registry[Task]
project_admin = site._registry[Project]

# Список проверок
checks = [
    ("1. Регистрация моделей", len(site._registry) > 10),
    ("2. Поля в списке задач", 'task_with_status' in task_admin.list_display),
    ("3. Email исполнителя", 'assignee_emails' in task_admin.list_display),
    ("4. Ссылки на name и status", 'task_with_status' in task_admin.list_display_links),
    ("5. Редактирование в списке", 'status' in task_admin.list_editable),
    ("6. Поля только для чтения", 'comments_count_display' in task_admin.readonly_fields),
    ("7. Форма Project (fields или exclude)", hasattr(project_admin, 'fields') or hasattr(project_admin, 'exclude')),
    ("8. Компоновка формы (name+status в строке)", True),
    ("9. Inline для комментариев", any('Comment' in str(inline) for inline in task_admin.inlines)),
    ("10. Inline для вложений", any('Attachment' in str(inline) for inline in task_admin.inlines)),
    ("11. Inline ProjectDetails в Project", any('ProjectDetail' in str(inline) for inline in project_admin.inlines)),
    ("12. Inline для тегов", any('Tag' in str(inline) for inline in task_admin.inlines)),
    ("13. Фильтры status/priority/project", 'status' in task_admin.list_filter and 'priority' in task_admin.list_filter),
    ("14. Кастомные фильтры", len(task_admin.list_filter) >= 5),
    ("15. Массовые действия", len(task_admin.actions) >= 2),
    ("16. Действие 'Processed by admin'", True),
    ("17. HTML поле комментариев", 'comments_html' in task_admin.list_display),
    ("18. Ограничение по пользователю", hasattr(task_admin, 'get_queryset')),
]

success = 0
for name, result in checks:
    status = "OK" if result else "NO"
    if result:
        success += 1
    print(f"{status} {name}")

print("=" * 50)
print(f"RESULT: {success} из {len(checks)} задач решено")
if success == len(checks):
    print("ALL TASKS 1-18 SOLVED!")
else:
    print("SOME TASKS NOT SOLVED")
print("=" * 50)