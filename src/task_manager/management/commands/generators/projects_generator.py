import random
from faker import Faker
from task_manager.models import Project

fake = Faker('ru_RU')


def generate_projects(self, stdout, count, users):
    """Создание проектов"""
    stdout.write('\n3. Создание проектов...')
    projects = []
    for i in range(count):
        project = Project.objects.create(
            name=fake.company(),
            description=fake.text(max_nb_chars=200),
            owner=random.choice(users)
        )
        projects.append(project)

    stdout.write(f'   Создано проектов: {len(projects)}')
    return projects