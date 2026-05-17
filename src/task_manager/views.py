from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from task_manager.models import Task, Comment, Attachment
from account.models import User
from .forms import (
    CommentForm, CommentWidgetForm,
    TaskCreateForm, TaskEditForm,
    TaskValidateForm, TaskWidgetForm,
    AttachmentUploadForm
)
import urllib.request

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


def upload_attachment(request):
    if request.method == 'POST':
        form = AttachmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.filename = request.FILES['file'].name
            attachment.save()
            messages.success(request, f'Файл "{attachment.filename}" успешно загружен!')
            return redirect('attachment_list')
    else:
        form = AttachmentUploadForm()

    return render(request, 'task_manager/upload.html', {'form': form})


def attachment_list(request):
    task_id = request.GET.get('task_id')

    if task_id:
        attachments = Attachment.objects.filter(task_id=task_id)
    else:
        attachments = Attachment.objects.all()

    paginator = Paginator(attachments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tasks = Task.objects.all()

    context = {
        'page_obj': page_obj,
        'tasks': tasks,
        'selected_task': task_id,
    }
    return render(request, 'task_manager/attachments.html', context)


def save_external_file(request):
    if request.method == 'POST':
        external_url = request.POST.get('url')
        task_id = request.POST.get('task_id')

        try:
            task = Task.objects.get(id=task_id)

            response = urllib.request.urlopen(external_url)
            file_content = response.read()

            filename = external_url.split('/')[-1]
            if not filename or '.' not in filename:
                filename = 'downloaded_file'

            attachment = Attachment(
                task=task,
                filename=filename
            )
            attachment.file.save(filename, ContentFile(file_content))
            attachment.save()

            messages.success(request, f'Файл "{filename}" успешно сохранён из внешнего пути!')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')

        return redirect('attachment_list')

    tasks = Task.objects.all()
    return render(request, 'task_manager/external_upload.html', {'tasks': tasks})


# ============================================
# GENERIC VIEWS
# ============================================

class HomeView(TemplateView):
    template_name = 'task_manager/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['total_tasks'] = Task.objects.count()
        context['total_users'] = User.objects.count()
        return context


class AboutView(TemplateView):
    template_name = 'task_manager/about.html'


class TasksListView(ListView):
    model = Task
    template_name = 'task_manager/tasks_list_generic.html'
    context_object_name = 'tasks'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        project_id = self.request.GET.get('project_id')

        if status:
            queryset = queryset.filter(status=status)
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset.select_related('project').prefetch_related('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from task_manager.models import Project
        context['statuses'] = Task.STATUS_CHOICES
        context['projects'] = Project.objects.all()
        context['current_status'] = self.request.GET.get('status', '')
        context['current_project'] = self.request.GET.get('project_id', '')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_manager/task_detail_generic.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['attachments'] = self.object.attachments.all()
        context['total_comments'] = context['comments'].count()
        return context


class UserTasksListView(ListView):
    model = Task
    template_name = 'task_manager/user_tasks_list_generic.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Task.objects.filter(users__id=user_id).select_related('project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['selected_user'] = User.objects.get(id=user_id)
        return context


class AttachmentListView(ListView):
    model = Attachment
    template_name = 'task_manager/attachments_list_generic.html'
    context_object_name = 'attachments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        task_id = self.request.GET.get('task_id')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset.select_related('task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['selected_task'] = self.request.GET.get('task_id', '')
        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task_manager/task_form_generic.html'
    success_url = reverse_lazy('tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание задачи (Generic)'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Задача "{self.object.title}" успешно создана!')
        return response


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'task_manager/comment_confirm_delete_generic.html'
    success_url = reverse_lazy('tasks_list')

    def get_success_url(self):
        task_id = self.object.task.id
        return reverse_lazy('task_detail', kwargs={'pk': task_id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Комментарий успешно удалён!')
        return super().delete(request, *args, **kwargs)