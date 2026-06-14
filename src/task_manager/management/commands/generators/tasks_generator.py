import random
from faker import Faker
from task_manager.models import Task

fake = Faker('ru_RU')


def generate_tasks(self, stdout, count, projects, users, tags):
    """Создание задач"""
    stdout.write('\n4. Создание задач...')
    statuses = ['created', 'started', 'completed', 'cancelled', 'reopened']
    priorities = [1, 2, 3, 4]
    tasks = []

    for i in range(count):
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
        tasks.append(task)

        if (i + 1) % 10000 == 0:
            stdout.write(f'   Создано задач: {i + 1}')

    stdout.write(f'   Создано задач: {count}')
    return tasks