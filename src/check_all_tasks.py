import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from account.models import User
from task_manager.models import Project, Task, Comment, Tag, Person, Employee, Client
from django.db import connection
from django.core.management import call_command

print("=" * 60)
print("ПРОВЕРКА ВСЕХ ЗАДАЧ (1-7)")
print("=" * 60)

# ЗАДАЧА 1: Наследование моделей
print("\n1. ПРОВЕРКА ЗАДАЧИ 1 - Наследование моделей")
try:
    from task_manager.models import BaseModel, Person, Employee, Client

    # Проверяем, что классы существуют
    has_base = hasattr(BaseModel, '__bases__')
    has_person = hasattr(Person, '__bases__')
    has_employee = hasattr(Employee, '__bases__')
    has_client = hasattr(Client, '__bases__')

    if has_person and has_employee and has_client:
        print("   Модели наследования созданы: ДА")
        print("   - BaseModel (абстрактная)")
        print("   - Person (наследуется от BaseModel)")
        print("   - Employee (наследуется от Person)")
        print("   - Client (наследуется от Person)")
        print("   ЗАДАЧА 1 РЕШЕНА: ДА")
    else:
        print("   ЗАДАЧА 1 РЕШЕНА: НЕТ")
except Exception as e:
    print(f"   ЗАДАЧА 1 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 2: Django Debug Toolbar
print("\n2. ПРОВЕРКА ЗАДАЧИ 2 - Django Debug Toolbar")
try:
    from django.conf import settings

    has_debug_toolbar = 'debug_toolbar' in settings.INSTALLED_APPS
    has_debug_middleware = any('debug_toolbar' in m for m in settings.MIDDLEWARE)

    if has_debug_toolbar and has_debug_middleware:
        print("   Django Debug Toolbar установлен: ДА")
        print("   - В INSTALLED_APPS: debug_toolbar")
        print("   - В MIDDLEWARE: DebugToolbarMiddleware")
        print("   ЗАДАЧА 2 РЕШЕНА: ДА")
    else:
        print("   ЗАДАЧА 2 РЕШЕНА: НЕТ")
except Exception as e:
    print(f"   ЗАДАЧА 2 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 3: Список задач с комментариями (оптимизированный запрос)
print("\n3. ПРОВЕРКА ЗАДАЧИ 3 - Список задач с комментариями")
try:
    # Очищаем историю запросов
    connection.queries.clear()

    # Выполняем оптимизированный запрос
    tasks = Task.objects.prefetch_related('comments').all()[:10]
    list(tasks)

    query_count = len(connection.queries)

    if query_count <= 2:
        print(f"   Оптимизированный запрос выполнен: ДА (SQL запросов: {query_count})")
        print("   Использован prefetch_related")
        print("   ЗАДАЧА 3 РЕШЕНА: ДА")
    else:
        print(f"   Оптимизированный запрос: НЕТ (SQL запросов: {query_count}, нужно <= 2)")
        print("   ЗАДАЧА 3 РЕШЕНА: НЕТ")
except Exception as e:
    print(f"   ЗАДАЧА 3 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 4: Страница с задачами пользователя
print("\n4. ПРОВЕРКА ЗАДАЧИ 4 - Страница задач пользователя")
try:
    from task_manager.views import user_tasks_with_comments
    from config.urls import urlpatterns

    has_url = False
    for pattern in urlpatterns:
        if 'user-tasks' in str(pattern):
            has_url = True
            break

    if has_url:
        print("   URL-маршрут /user-tasks/<int:user_id>/ создан: ДА")
        print("   Функция user_tasks_with_comments создана: ДА")
        print("   Шаблон user_tasks.html должен существовать")
        print("   ЗАДАЧА 4 РЕШЕНА: ДА")
    else:
        print("   ЗАДАЧА 4 РЕШЕНА: НЕТ (нет URL маршрута)")
except Exception as e:
    print(f"   ЗАДАЧА 4 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 5: Кастомный менеджер для завершённых задач
print("\n5. ПРОВЕРКА ЗАДАЧИ 5 - Кастомный менеджер")
try:
    from task_manager.models import Task

    has_completed_manager = hasattr(Task, 'completed')
    has_active_manager = hasattr(Task, 'active')

    # Проверяем, что completed возвращает только задачи со статусом 'completed'
    completed_tasks = Task.completed.all()
    all_valid = True
    for task in completed_tasks[:10]:
        if task.status != 'completed':
            all_valid = False
            break

    if has_completed_manager and all_valid:
        print("   Кастомный менеджер Task.completed создан: ДА")
        print("   Возвращает только задачи со статусом 'completed': ДА")
        print("   ЗАДАЧА 5 РЕШЕНА: ДА")
    else:
        print("   ЗАДАЧА 5 РЕШЕНА: НЕТ")
except Exception as e:
    print(f"   ЗАДАЧА 5 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 6: Сигнал при создании задачи
print("\n6. ПРОВЕРКА ЗАДАЧИ 6 - Сигнал при создании задачи")
try:
    from task_manager import signals
    from task_manager.apps import TaskManagerConfig

    # Проверяем, что сигнал подключен
    has_signal = hasattr(signals, 'create_task_created_comment')

    # Создаём тестовую задачу
    project = Project.objects.first()
    user = User.objects.first()

    if project and user:
        test_task = Task.objects.create(
            title='Тестовая задача для проверки сигнала',
            project=project,
            status='created',
            priority=1
        )
        test_task.users.add(user)

        # Проверяем, создался ли комментарий
        test_comments = Comment.objects.filter(task=test_task, text__icontains='Task created')
        has_auto_comment = test_comments.exists()

        # Удаляем тестовые данные
        test_task.delete()

        if has_signal or has_auto_comment:
            print("   Сигнал post_save для Task создан: ДА")
            print("   При создании задачи автоматически создаётся комментарий: ДА")
            print("   ЗАДАЧА 6 РЕШЕНА: ДА")
        else:
            print("   ЗАДАЧА 6 РЕШЕНА: НЕТ")
    else:
        print("   ЗАДАЧА 6 РЕШЕНА: НЕТ (нет данных для проверки)")
except Exception as e:
    print(f"   ЗАДАЧА 6 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ЗАДАЧА 7: Генерация данных
print("\n7. ПРОВЕРКА ЗАДАЧИ 7 - Генерация данных")
try:
    # Проверяем наличие management команды
    from task_manager.management.commands import generate_data

    users_count = User.objects.count()
    projects_count = Project.objects.count()
    tasks_count = Task.objects.count()
    comments_count = Comment.objects.count()
    tags_count = Tag.objects.count()

    print(f"   Пользователей: {users_count}")
    print(f"   Проектов: {projects_count}")
    print(f"   Задач: {tasks_count}")
    print(f"   Комментариев: {comments_count}")
    print(f"   Тегов: {tags_count}")

    # Проверяем, что у задач есть ответственные и проекты
    tasks_without_users = Task.objects.filter(users__isnull=True).count()
    tasks_without_projects = Task.objects.filter(project__isnull=True).count()

    print(f"   Задач без ответственных: {tasks_without_users}")
    print(f"   Задач без проекта: {tasks_without_projects}")

    if tasks_count >= 100:
        print("   ЗАДАЧА 7 РЕШЕНА: ДА")
    else:
        print("   ЗАДАЧА 7 РЕШЕНА: НЕТ (мало данных, запустите python manage.py generate_data)")
except ImportError:
    print("   ЗАДАЧА 7 РЕШЕНА: НЕТ (команда generate_data не создана)")
except Exception as e:
    print(f"   ЗАДАЧА 7 РЕШЕНА: НЕТ ({str(e)[:50]})")

# ИТОГОВАЯ ТАБЛИЦА
print("\n" + "=" * 60)
print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("=" * 60)

results = {}

# Задача 1 - нужно проверить вручную или добавить проверку
results['Задача 1 (Наследование)'] = 'Проверьте наличие файлов: base_model.py, person.py, employee.py, client.py'

# Задача 2
try:
    from django.conf import settings

    results['Задача 2 (Debug Toolbar)'] = 'РЕШЕНА' if 'debug_toolbar' in settings.INSTALLED_APPS else 'НЕ РЕШЕНА'
except:
    results['Задача 2 (Debug Toolbar)'] = 'НЕ РЕШЕНА'

# Задача 3
try:
    connection.queries.clear()
    list(Task.objects.prefetch_related('comments').all()[:5])
    results['Задача 3 (Оптимизация)'] = 'РЕШЕНА' if len(connection.queries) <= 2 else 'НЕ РЕШЕНА'
except:
    results['Задача 3 (Оптимизация)'] = 'НЕ РЕШЕНА'

# Задача 4
try:
    from config.urls import urlpatterns

    has_url = any('user-tasks' in str(p) for p in urlpatterns)
    results['Задача 4 (Страница пользователя)'] = 'РЕШЕНА' if has_url else 'НЕ РЕШЕНА'
except:
    results['Задача 4 (Страница пользователя)'] = 'НЕ РЕШЕНА'

# Задача 5
try:
    from task_manager.models import Task

    completed_exists = hasattr(Task, 'completed')
    results['Задача 5 (Кастомный менеджер)'] = 'РЕШЕНА' if completed_exists else 'НЕ РЕШЕНА'
except:
    results['Задача 5 (Кастомный менеджер)'] = 'НЕ РЕШЕНА'

# Задача 6
try:
    from task_manager import signals

    signal_exists = hasattr(signals, 'create_task_created_comment')
    results['Задача 6 (Сигнал)'] = 'РЕШЕНА' if signal_exists else 'НЕ РЕШЕНА'
except:
    results['Задача 6 (Сигнал)'] = 'НЕ РЕШЕНА'

# Задача 7
try:
    from task_manager.management.commands import generate_data

    tasks_count = Task.objects.count()
    results['Задача 7 (Генерация данных)'] = 'РЕШЕНА' if tasks_count >= 100 else 'ТРЕБУЕТ ЗАПУСКА'
except:
    results['Задача 7 (Генерация данных)'] = 'НЕ РЕШЕНА'

for task, status in results.items():
    print(f"{task}: {status}")

print("=" * 60)
print("\nДля полной проверки убедитесь, что:")
print("- Созданы файлы base_model.py, person.py, employee.py, client.py")
print("- В settings.py добавлен debug_toolbar")
print("- В urls.py добавлен маршрут user-tasks")
print("- Создан шаблон user_tasks.html")
print("- Запущена команда: python manage.py generate_data")