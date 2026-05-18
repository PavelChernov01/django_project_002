from django.urls import path
from .api_views import (
    TaskListAPIView, TaskDetailAPIView, TaskCreateAPIView, TaskUpdateAPIView, TaskDeleteAPIView,
    TagListAPIView, TagDetailAPIView,
    ProjectListCreateAPIView, ProjectRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView,
    AttachmentListCreateAPIView, AttachmentRetrieveDestroyAPIView
)

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
]