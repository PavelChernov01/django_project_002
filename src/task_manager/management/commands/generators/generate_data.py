from django.core.management.base import BaseCommand
from .generators.tags_generator import generate_tags
from .generators.users_generator import generate_users
from .generators.projects_generator import generate_projects
from .generators.tasks_generator import generate_tasks
from .generators.comments_generator import generate_comments
from task_manager.models import User, Project, Task, Comment, Tag


class Command(BaseCommand):
    help = 'Генерирует тестовые данные'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=100, help='Количество пользователей')
        parser.add_argument('--projects', type=int, default=10, help='Количество проектов')
        parser.add_argument('--tasks', type=int, default=1000000, help='Количество задач')

    def handle(self, *args, **options):
        users_count = options['users']
        projects_count = options['projects']
        tasks_count = options['tasks']

        self.stdout.write('Начинаем генерацию данных...')
        self.stdout.write(f'Пользователей: {users_count}')
        self.stdout.write(f'Проектов: {projects_count}')
        self.stdout.write(f'Задач: {tasks_count}')

        # Вызов генераторов
        tags = generate_tags(self, self.stdout)
        users = generate_users(self, self.stdout, users_count)
        projects = generate_projects(self, self.stdout, projects_count, users)
        tasks = generate_tasks(self, self.stdout, tasks_count, projects, users, tags)
        generate_comments(self, self.stdout, tasks, users)

        # Итог
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('ГЕНЕРАЦИЯ ЗАВЕРШЕНА!')
        self.stdout.write('=' * 50)
        self.stdout.write(f'Пользователей: {User.objects.count()}')
        self.stdout.write(f'Проектов: {Project.objects.count()}')
        self.stdout.write(f'Задач: {Task.objects.count()}')
        self.stdout.write(f'Комментариев: {Comment.objects.count()}')
        self.stdout.write(f'Тегов: {Tag.objects.count()}')
        self.stdout.write('=' * 50)