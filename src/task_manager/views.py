from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from task_manager.models import Task, Comment
from account.models import User

# Ваши существующие данные
tasks_data = [
    {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
    {"task_name": "Create navbar", "status": "done", "priority": "medium"},
    {"task_name": "Write tests", "status": "todo", "priority": "high"},
    {"task_name": "Update documentation", "status": "todo", "priority": "low"},
    {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
]

users_data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 28},
    {"name": "Diana", "age": 22}
]


def home(request):
    """Главная страница"""
    return render(request, 'task_manager/home.html')


def tasks_list(request):
    """Страница со списком задач"""
    return render(request, 'task_manager/tasks.html', {'tasks': tasks_data})


def users_list(request):
    """Страница со списком пользователей"""
    # Получаем пользователей из базы данных
    db_users = User.objects.all()
    return render(request, 'task_manager/users.html', {
        'users': db_users,
        'users_data': users_data
    })


def user_tasks_with_comments(request, user_id):
    """Страница с задачами и комментариями выбранного пользователя"""

    # Получаем выбранного пользователя из базы данных
    user = get_object_or_404(User, id=user_id)

    # Оптимизированный запрос: получаем задачи пользователя и сразу подгружаем комментарии
    tasks = Task.objects.filter(users=user).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    )

    # Для каждой задачи собираем комментарии этого пользователя
    tasks_with_user_comments = []
    for task in tasks:
        user_comments = task.comments.filter(author=user)
        tasks_with_user_comments.append({
            'task': task,
            'comments': user_comments,
            'comments_count': user_comments.count()
        })

    context = {
        'selected_user': user,
        'tasks_data': tasks_with_user_comments,
        'total_tasks': tasks.count(),
    }

    return render(request, 'task_manager/user_tasks.html', context)