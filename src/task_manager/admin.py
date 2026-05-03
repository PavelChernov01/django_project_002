from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project, ProjectDetail, Task,
    Comment, Attachment, Tag
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Настройка отображения модели Project в админке"""

    list_display = ('id', 'name', 'owner', 'created_at', 'tasks_count')
    list_display_links = ('id', 'name')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'description', 'owner__phone', 'owner__first_name')
    list_per_page = 20
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('name', 'description', 'owner')}),
        ('Даты', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def tasks_count(self, obj):
        """Количество задач в проекте"""
        return obj.tasks.count()

    tasks_count.short_description = 'Количество задач'


@admin.register(ProjectDetail)
class ProjectDetailAdmin(admin.ModelAdmin):
    """Настройка отображения модели ProjectDetail в админке"""

    list_display = ('id', 'project', 'budget', 'deadline', 'repository_url')
    list_display_links = ('id', 'project')
    list_filter = ('deadline',)
    search_fields = ('project__name', 'repository_url')
    list_per_page = 20
    list_editable = ('budget', 'deadline')

    fieldsets = (
        (None, {'fields': ('project',)}),
        ('Финансы', {'fields': ('budget',)}),
        ('Сроки', {'fields': ('deadline',)}),
        ('Ссылки', {'fields': ('repository_url',)}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка отображения модели Tag в админке"""

    list_display = ('id', 'name', 'slug', 'tasks_count')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('name', 'slug')}),
    )

    def tasks_count(self, obj):
        """Количество задач с этим тегом"""
        return obj.tasks.count()

    tasks_count.short_description = 'Количество задач'


class TaskTagInline(admin.TabularInline):
    """Inline для отображения тегов внутри задачи"""
    model = Task.tags.through
    extra = 1
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class TaskUserInline(admin.TabularInline):
    """Inline для отображения пользователей внутри задачи"""
    model = Task.users.through
    extra = 1
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


class CommentInline(admin.TabularInline):
    """Inline для отображения комментариев внутри задачи"""
    model = Comment
    extra = 1
    fields = ('author', 'text', 'created_at')
    readonly_fields = ('created_at',)
    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии'


class AttachmentInline(admin.TabularInline):
    """Inline для отображения вложений внутри задачи"""
    model = Attachment
    extra = 1
    fields = ('filename', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    verbose_name = 'Вложение'
    verbose_name_plural = 'Вложения'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Настройка отображения модели Task в админке"""

    list_display = (
        'id', 'title', 'project', 'status',
        'priority_display', 'created_at'
    )
    list_display_links = ('id', 'title')
    list_filter = ('status', 'priority', 'created_at', 'project')
    search_fields = ('title', 'description', 'project__name')
    list_per_page = 20
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')

    # Inline модели
    inlines = [TaskTagInline, TaskUserInline, CommentInline, AttachmentInline]

    fieldsets = (
        (None, {'fields': ('title', 'description', 'project')}),
        ('Статус и приоритет', {'fields': ('status', 'priority')}),
        ('Назначения', {'fields': ('users', 'tags')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )

    filter_horizontal = ('users', 'tags')

    def priority_display(self, obj):
        """Отображение приоритета цветом"""
        colors = {
            1: 'green',
            2: 'orange',
            3: 'red',
            4: 'darkred',
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )

    priority_display.short_description = 'Приоритет'
    priority_display.admin_order_field = 'priority'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка отображения модели Comment в админке"""

    list_display = ('id', 'task', 'author', 'text_preview', 'created_at')
    list_display_links = ('id', 'task')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'task__title', 'author__phone')
    list_per_page = 20
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('task', 'author', 'text')}),
        ('Дата', {'fields': ('created_at',)}),
    )

    def text_preview(self, obj):
        """Предварительный просмотр текста комментария"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст (предпросмотр)'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Настройка отображения модели Attachment в админке"""

    list_display = ('id', 'filename', 'task', 'uploaded_at')
    list_display_links = ('id', 'filename')
    list_filter = ('uploaded_at', 'task')
    search_fields = ('filename', 'task__title')
    list_per_page = 20
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        (None, {'fields': ('task', 'filename', 'file')}),
        ('Дата', {'fields': ('uploaded_at',)}),
    )