from django.test import TestCase, Client
from account.models import User
from task_manager.models import Project, Task


class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            phone='+79999999999',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='test123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            project=self.project,
            status='created',
            priority=2
        )
        self.task.users.add(self.user)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_tasks_list_page(self):
        response = self.client.get('/tasks-list/')
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_page(self):
        response = self.client.get(f'/task-detail/{self.task.id}/')
        self.assertEqual(response.status_code, 200)

    def test_users_list_page(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_task_create_page_exists(self):
        """Тест: страница создания задачи существует"""
        response = self.client.get('/task/create/')
        self.assertEqual(response.status_code, 200)