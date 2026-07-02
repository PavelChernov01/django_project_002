import random
from django.core.management.base import BaseCommand
from faker import Faker
from account.models import User
from task_manager.models import Project, Task, Comment, Tag

fake = Faker('ru_RU')


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

        # 1. Теги
        self.stdout.write('\n1. Создание тегов...')
        Tag.objects.all().delete()

        tag_names = ['bug', 'feature', 'urgent', 'test', 'deploy', 'security', 'documentation']
        tags = []
        for name in tag_names:
            tag = Tag(name=name)
            tag.save()
            tags.append(tag)
            self.stdout.write(f'   Создан тег: {name}')

        # 2. Пользователи
        self.stdout.write('\n2. Создание пользователей...')
        users = []
        for i in range(users_count):
            user = User(
                phone=fake.unique.phone_number(),
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True
            )
            user.set_password('password123')
            user.save()
            users.append(user)

            if (i + 1) % 100 == 0:
                self.stdout.write(f'   Создано пользователей: {i + 1}')

        self.stdout.write(f'   Создано пользователей: {len(users)}')

        # 3. Проекты
        self.stdout.write('\n3. Создание проектов...')
        projects = []
        for i in range(projects_count):
            project = Project.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                owner=random.choice(users)
            )
            projects.append(project)

        self.stdout.write(f'   Создано проектов: {len(projects)}')

        # 4. Задачи
        self.stdout.write('\n4. Создание задач...')
        statuses = ['created', 'started', 'completed', 'cancelled', 'reopened']
        priorities = [1, 2, 3, 4]

        for i in range(tasks_count):
            task = Task(
                title=fake.sentence(nb_words=6)[:200],
                description=fake.text(max_nb_chars=500),
                status=random.choice(statuses),
                priority=random.choice(priorities),
                project=random.choice(projects)
            )
            task.save()

            responsible_users = random.sample(users, k=random.randint(1, 3))
            task.users.set(responsible_users)

            task.tags.set(random.sample(tags, k=random.randint(0, min(3, len(tags)))))

            if (i + 1) % 10000 == 0:
                self.stdout.write(f'   Создано задач: {i + 1}')

        self.stdout.write(f'   Создано задач: {tasks_count}')

        # 5. Комментарии
        self.stdout.write('\n5. Создание комментариев...')
        comments_count = 0
        tasks_for_comments = Task.objects.all()[:min(10000, tasks_count)]

        for task in tasks_for_comments:
            num_comments = random.randint(0, 5)
            for _ in range(num_comments):
                Comment.objects.create(
                    text=fake.text(max_nb_chars=200),
                    task=task,
                    author=random.choice(users)
                )
                comments_count += 1

            if comments_count % 10000 == 0 and comments_count > 0:
                self.stdout.write(f'   Создано комментариев: {comments_count}')

        self.stdout.write(f'   Создано комментариев: {comments_count}')

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