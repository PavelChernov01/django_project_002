from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from .models import (
    Project, ProjectDetail, Task,
    Comment, Attachment, Tag, Person, Employee, Client
)
from .models import Attachment


# ============================================
# ЗАДАЧА 14:
# ============================================

class AssigneeFilter(SimpleListFilter):
    title = 'Исполнитель'
    parameter_name = 'assignee'

    def lookups(self, request, model_admin):
        users_with_tasks = set()
        for task in Task.objects.all():
            for user in task.users.all():
                users_with_tasks.add(user)
        return [(user.id, f"{user.first_name} {user.last_name}") for user in users_with_tasks]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(users__id=self.value())
        return queryset


class EmptyAssigneeFilter(SimpleListFilter):
    title = 'Наличие исполнителя'
    parameter_name = 'has_assignee'

    def lookups(self, request, model_admin):
        return (('yes', 'Есть исполнитель'), ('no', 'Нет исполнителя'))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(users__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(users__isnull=True)
        return queryset


# ============================================
# ЗАДАЧА 15-16:
# ============================================

def mark_as_completed(modeladmin, request, queryset):
    updated = queryset.update(status='completed')
    modeladmin.message_user(request, f'{updated} задач отмечены как завершённые')
mark_as_completed.short_description = 'Отметить задачи как завершённые'


def mark_as_cancelled(modeladmin, request, queryset):
    updated = queryset.update(status='cancelled')
    modeladmin.message_user(request, f'{updated} задач отмечены как отменённые')
mark_as_cancelled.short_description = 'Отметить задачи как отменённые'


def add_admin_comment(modeladmin, request, queryset):
    count = 0
    for task in queryset:
        Comment.objects.create(task=task, author=request.user, text="Processed by admin")
        count += 1
    modeladmin.message_user(request, f'Добавлено {count} комментариев')
add_admin_comment.short_description = 'Добавить комментарий "Processed by admin"'


# ============================================
# INLINE КЛАССЫ
# ============================================

class TaskTagInline(admin.TabularInline):
    """ЗАДАЧА 12: Inline для тегов"""
    model = Task.tags.through
    extra = 1
    verbose_name = 'Тег'


class TaskUserInline(admin.TabularInline):
    model = Task.users.through
    extra = 1
    verbose_name = 'Пользователь'


class CommentInline(admin.TabularInline):
    """ЗАДАЧА 9: Inline для комментариев"""
    model = Comment
    extra = 1
    fields = ('author', 'text', 'created_at')
    readonly_fields = ('created_at',)
    verbose_name = 'Комментарий'


class AttachmentInline(admin.TabularInline):
    """ЗАДАЧА 10: Inline для вложений"""
    model = Attachment
    extra = 1
    fields = ('filename', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    verbose_name = 'Вложение'


class ProjectDetailInline(admin.StackedInline):
    """ЗАДАЧА 11: Inline для деталей проекта (StackedInline - компактно для 3 полей)"""
    model = ProjectDetail
    extra = 1
    verbose_name = 'Детали проекта'
    fields = ('budget', 'deadline', 'repository_url')


# ============================================
# ЗАДАЧА 1 + 7:
# ============================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = ('name', 'description')  # ЗАДАЧА 7: через fields
    list_display = ('id', 'name', 'owner', 'created_at')
    inlines = [ProjectDetailInline]  # ЗАДАЧА 11


@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'budget', 'deadline')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


# ============================================
# ЗАДАЧА 18:
# ============================================

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    # ЗАДАЧА 2: Поля в списке
    list_display = (
        'id',
        'task_with_status',
        'status',
        'priority_display',
        'project',
        'assignee_list',
        'assignee_emails',
        'created_at',
        'comments_count',
        'comments_html',
    )

    # ЗАДАЧА 4: Ссылки только на name и status
    list_display_links = ('task_with_status',)

    # ЗАДАЧА 5: Редактирование в списке
    list_editable = ('status',)

    # ЗАДАЧА 13-14: Фильтры
    list_filter = ('status', 'priority', 'project', AssigneeFilter, EmptyAssigneeFilter)

    search_fields = ('title', 'description', 'project__name')
    list_per_page = 20

    # ЗАДАЧА 6: Поля только для чтения
    readonly_fields = ('created_at', 'updated_at', 'comments_count_display', 'comments_html')

    # ЗАДАЧА 15-16: Массовые действия
    actions = [mark_as_completed, mark_as_cancelled, add_admin_comment]

    # ЗАДАЧА 9,10,12: Inline
    inlines = [TaskTagInline, TaskUserInline, CommentInline, AttachmentInline]

    # ЗАДАЧА 8: Компоновка формы
    fieldsets = (
        (None, {
            'fields': (
                ('title', 'status'),
                'description',
                'priority',
                'project',
            )
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'comments_count_display'),
            'classes': ('collapse',),
        }),
        ('Комментарии', {
            'fields': ('comments_html',),
            'classes': ('collapse',),
        }),
    )

    filter_horizontal = ('users', 'tags')

    # ЗАДАЧА 18:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users=request.user)

    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========

    def priority_display(self, obj):
        colors = {1: 'green', 2: 'orange', 3: 'red', 4: 'darkred'}
        return mark_safe(f'<span style="color: {colors.get(obj.priority, "black")};">{obj.get_priority_display()}</span>')
    priority_display.short_description = 'Приоритет'
    priority_display.admin_order_field = 'priority'

    def task_with_status(self, obj):
        colors = {'created': 'gray', 'started': 'blue', 'completed': 'green', 'cancelled': 'red', 'reopened': 'orange'}
        return mark_safe(f'<b>{obj.title}</b> <span style="color: {colors.get(obj.status, "black")};">({obj.get_status_display()})</span>')
    task_with_status.short_description = 'Задача'
    task_with_status.admin_order_field = 'title'

    def assignee_list(self, obj):
        names = [f"{u.first_name} {u.last_name}".strip() or u.phone for u in obj.users.all()]
        return ', '.join(names) if names else '-'
    assignee_list.short_description = 'Исполнители'

    @admin.display(description='Email', ordering='users__email')
    def assignee_emails(self, obj):
        emails = [u.email for u in obj.users.all() if u.email]
        return ', '.join(emails) if emails else '-'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Комментариев'
    comments_count.admin_order_field = 'comments_count'

    def comments_count_display(self, obj):
        count = obj.comments.count()
        if count % 10 == 1 and count % 100 != 11:
            word = 'комментарий'
        elif count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
            word = 'комментария'
        else:
            word = 'комментариев'
        return mark_safe(f'<strong>{count}</strong> {word}')
    comments_count_display.short_description = 'Всего комментариев'

    def comments_html(self, obj):
        comments = obj.comments.all().order_by('-created_at')
        if not comments:
            return 'Нет комментариев'
        html = '<div style="max-height:250px;overflow:auto;">'
        for c in comments:
            html += f'<div style="border-bottom:1px solid #eee;padding:5px;"><b>{c.author}</b> <small>({c.created_at.strftime("%d.%m.%Y %H:%M")})</small><br>{c.text}</div>'
        html += '</div>'
        return mark_safe(html)
    comments_html.short_description = 'Список комментариев'


# ============================================
# ЗАДАЧА 1:
# ============================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'text_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'task__title')

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'task', 'uploaded_at', 'image_preview')
    list_display_links = ('id', 'filename')
    list_filter = ('uploaded_at', 'task')
    search_fields = ('filename', 'task__title')
    list_per_page = 20
    readonly_fields = ('uploaded_at', 'image_preview')

    fieldsets = (
        (None, {'fields': ('task', 'filename', 'file')}),
        ('Дата', {'fields': ('uploaded_at',)}),
        ('Предпросмотр', {'fields': ('image_preview',)}),
    )

    def image_preview(self, obj):
        if obj.file:
            if obj.is_image():
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px; max-width: 200px;" />')
            else:
                return mark_safe(f'<a href="{obj.file.url}">Скачать {obj.filename}</a>')
        return 'Нет файла'
    image_preview.short_description = 'Предпросмотр'

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'position', 'employee_id')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'client_id', 'discount')
