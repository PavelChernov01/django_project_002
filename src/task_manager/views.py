from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.contrib import messages
from task_manager.models import Task, Comment
from account.models import User
from .forms import (
    CommentForm, CommentWidgetForm,
    TaskCreateForm, TaskEditForm,
    TaskValidateForm, TaskWidgetForm
)


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
    return render(request, 'task_manager/home.html')


def tasks_list(request):
    return render(request, 'task_manager/tasks.html', {'tasks': tasks_data})


def users_list(request):
    db_users = User.objects.all()
    return render(request, 'task_manager/users.html', {
        'users': db_users,
        'users_data': users_data
    })


def user_tasks_with_comments(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(users=user).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    )
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

# ============================================

def comment_form_view(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            user = form.cleaned_data['user']
            messages.success(request, f'Комментарий от {user}: {message[:50]}...')
            return redirect('comment_form')
    return render(request, 'task_manager/comment_form.html', {'form': form})


def comment_widget_view(request):
    form = CommentWidgetForm()
    if request.method == 'POST':
        form = CommentWidgetForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Комментарий отправлен!')
            return redirect('comment_widget')
    return render(request, 'task_manager/comment_widget.html', {'form': form})


def task_create_view(request, task_id=None):
    task = None
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        form = TaskValidateForm(request.POST or None, instance=task)
    else:
        form = TaskCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        task = form.save()
        messages.success(request, f'Задача "{task.title}" успешно сохранена!')
        return redirect('task_create')

    return render(request, 'task_manager/task_form.html', {'form': form, 'task': task})


def task_widget_view(request):
    form = TaskWidgetForm()
    if request.method == 'POST':
        form = TaskWidgetForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Задача "{task.title}" создана!')
            return redirect('task_widget')
    return render(request, 'task_manager/task_widget.html', {'form': form})


def task_crispy_view(request):
    form = TaskCreateForm()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Задача "{task.title}" создана!')
            return redirect('task_crispy')
    return render(request, 'task_manager/task_crispy.html', {'form': form})