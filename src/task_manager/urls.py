
from django.urls import path
from task_manager.views import index, tasks_list, users_list

urlpatterns = [
    path('', tasks_list, name='tasks'),      # /tasks/
    path('users/', users_list, name='users'), # /tasks/users/
]
