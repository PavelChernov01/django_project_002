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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.tasks_list, name='tasks'),
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
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()
