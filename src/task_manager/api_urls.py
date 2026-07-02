from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    TaskListAPIView, TaskDetailAPIView, TaskCreateAPIView, TaskUpdateAPIView, TaskDeleteAPIView,
    TagListAPIView, TagDetailAPIView,
    ProjectListCreateAPIView, ProjectRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView,
    AttachmentListCreateAPIView, AttachmentRetrieveDestroyAPIView,
    ObtainAuthTokenView, ProtectedTaskListView, get_user_info,
    UserListView, TaskListView, MyTaskListView, TaskDateFilterView,
    PeriodicTaskViewSet, IntervalScheduleViewSet, CrontabScheduleViewSet, SolarScheduleViewSet
)

# Создаём роутер для Celery Beat
router = DefaultRouter()
router.register(r'periodic-tasks', PeriodicTaskViewSet, basename='periodic-tasks')
router.register(r'intervals', IntervalScheduleViewSet, basename='intervals')
router.register(r'crontabs', CrontabScheduleViewSet, basename='crontabs')
router.register(r'solar', SolarScheduleViewSet, basename='solar')

urlpatterns = [
    # Задачи (4 основных запроса)
    path('tasks/', TaskListAPIView.as_view(), name='api_tasks_list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api_task_detail'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='api_task_create'),
    path('tasks/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='api_task_update'),
    path('tasks/delete/<int:pk>/', TaskDeleteAPIView.as_view(), name='api_task_delete'),

    # Теги
    path('tags/', TagListAPIView.as_view(), name='api_tags_list'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='api_tag_detail'),

    # Проекты
    path('projects/', ProjectListCreateAPIView.as_view(), name='api_projects'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='api_project_detail'),

    # Комментарии
    path('comments/', CommentListCreateAPIView.as_view(), name='api_comments'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='api_comment_detail'),

    # Вложения
    path('attachments/', AttachmentListCreateAPIView.as_view(), name='api_attachments'),
    path('attachments/<int:pk>/', AttachmentRetrieveDestroyAPIView.as_view(), name='api_attachment_detail'),

    # ============================================
    # TOKEN AUTHENTICATION (ЗАДАЧА 5)
    # ============================================
    path('auth/token/', ObtainAuthTokenView.as_view(), name='api_obtain_token'),
    path('protected-tasks/', ProtectedTaskListView.as_view(), name='api_protected_tasks'),
    path('auth/user/', get_user_info, name='api_user_info'),

    # ============================================
    # НОВЫЕ МАРШРУТЫ ДЛЯ ФИЛЬТРАЦИИ И ПАГИНАЦИИ
    # ============================================
    path('users/', UserListView.as_view(), name='api_users_list'),
    path('tasks-filter/', TaskListView.as_view(), name='api_tasks_filter'),
    path('my-tasks/', MyTaskListView.as_view(), name='api_my_tasks'),
    path('tasks-date-filter/', TaskDateFilterView.as_view(), name='api_tasks_date_filter'),

    # ============================================
    # CELERY BEAT API (ЗАДАЧА 8)
    # ============================================
    path('', include(router.urls)),
]