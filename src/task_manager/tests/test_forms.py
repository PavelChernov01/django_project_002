from django.test import TestCase
from account.models import User  # Исправлено
from task_manager.forms import TaskCreateForm, TaskValidateForm, CommentForm, TaskWidgetForm
from task_manager.models import Project


class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone='+79999999999',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='test123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )

    def test_task_create_form_valid(self):
        form_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'created',
            'priority': 2,
            'project': self.project.id
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_invalid(self):
        form_data = {
            'title': '',
            'description': 'Test',
            'status': 'created',
            'priority': 2,
            'project': self.project.id
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_validate_form_valid(self):
        form_data = {
            'title': 'High Priority Task',
            'description': 'Important description',
            'status': 'created',
            'priority': 4,
            'project': self.project.id
        }
        form = TaskValidateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_validate_form_invalid(self):
        form_data = {
            'title': 'High Priority Task',
            'description': '',
            'status': 'created',
            'priority': 4,
            'project': self.project.id
        }
        form = TaskValidateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        form_data = {
            'message': 'Test comment message',
            'user': self.user.id
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {
            'message': '',
            'user': self.user.id
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_widget_form_valid(self):
        form_data = {
            'title': 'Widget Task',
            'description': 'Widget description',
            'status': 'created',
            'priority': 3,
            'project': self.project.id
        }
        form = TaskWidgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_widget_form_invalid(self):
        form_data = {
            'title': 'Widget Task',
            'description': 'Widget description',
            'status': 'created',
            'priority': 3,
            'project': ''
        }
        form = TaskWidgetForm(data=form_data)
        self.assertFalse(form.is_valid())