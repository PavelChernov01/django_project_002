"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for config project.
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from task_manager import views
from task_manager.views import (
    HomeView, AboutView, TasksListView, TaskDetailView, TaskCreateView,
    UserTasksListView, AttachmentListView, CommentDeleteView
)

# Импорты для кэша
from task_manager.cache_examples import (
    test_lru_cache, cached_tasks_list, cached_projects_list,
    invalidate_task_cache, cached_statistics_block, invalidate_file_cache
)

# Импорты для DRF документации
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # ============================================
    # API ДОКУМЕНТАЦИЯ (DRF SPECTACULAR)
    # ============================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ============================================
    # API ENDPOINTS
    # ============================================
    path('api/', include('task_manager.api_urls')),

    # ============================================
    # GENERIC VIEWS (НОВЫЕ)
    # ============================================
    path('', HomeView.as_view(), name='home_generic'),
    path('about/', AboutView.as_view(), name='about'),
    path('tasks-list/', TasksListView.as_view(), name='tasks_list'),
    path('task-detail/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task-create/', TaskCreateView.as_view(), name='task_create_generic'),
    path('user-tasks-list/<int:user_id>/', UserTasksListView.as_view(), name='user_tasks_list'),
    path('attachments-list/', AttachmentListView.as_view(), name='attachment_list_generic'),
    path('comment-delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),

    # ============================================
    # ЗАДАЧИ ПО КЭШИРОВАНИЮ (CACHE)
    # ============================================
    path('cache/lru-test/', test_lru_cache, name='lru_test'),
    path('cache/tasks/', cached_tasks_list, name='cached_tasks'),
    path('cache/projects/', cached_projects_list, name='cached_projects'),
    path('cache/invalidate/', invalidate_task_cache, name='invalidate_cache'),
    path('cache/statistics/', cached_statistics_block, name='cached_statistics'),
    path('cache/invalidate-file/', invalidate_file_cache, name='invalidate_file_cache'),

    # ============================================
    # СТАРЫЕ VIEWS
    # ============================================
    path('old/', views.home, name='home'),
    path('old/tasks/', views.tasks_list, name='tasks'),
    path('users/', views.users_list, name='users'),
    path('user-tasks/<int:user_id>/', views.user_tasks_with_comments, name='user_tasks'),

    # ЗАДАЧА 1-2: Формы комментариев
    path('comment/', views.comment_form_view, name='comment_form'),
    path('comment-widget/', views.comment_widget_view, name='comment_widget'),

    # ЗАДАЧА 3-6: Формы задач
    path('task/create/', views.task_create_view, name='task_create'),
    path('task/edit/<int:task_id>/', views.task_create_view, name='task_edit'),
    path('task/widget/', views.task_widget_view, name='task_widget'),

    # ЗАДАЧА 7: Crispy forms
    path('task/crispy/', views.task_crispy_view, name='task_crispy'),

    # ЗАДАЧА 1-9: Медиафайлы и вложения
    path('attachments/', views.attachment_list, name='attachment_list'),
    path('upload/', views.upload_attachment, name='upload_attachment'),
    path('external-upload/', views.save_external_file, name='external_upload'),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns = [*urlpatterns] + debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)