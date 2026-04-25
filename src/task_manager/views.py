
# from django.http import HttpResponse

from django.shortcuts import render

tasks = [
    {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
    {"task_name": "Create navbar", "status": "done", "priority": "medium"},
    {"task_name": "Write tests", "status": "todo", "priority": "high"},
    {"task_name": "Update documentation", "status": "todo", "priority": "low"},
    {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
]

users = [
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
    return render(request, 'task_manager/tasks.html', {'tasks': tasks})

def users_list(request):
    """Страница со списком пользователей"""
    return render(request, 'task_manager/users.html', {'users': users})