import random
from faker import Faker
from task_manager.models import Comment

fake = Faker('ru_RU')


def generate_comments(self, stdout, tasks, users):
    """Создание комментариев"""
    stdout.write('\n5. Создание комментариев...')
    comments_count = 0
    tasks_for_comments = tasks[:min(10000, len(tasks))]

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
            stdout.write(f'   Создано комментариев: {comments_count}')

    stdout.write(f'   Создано комментариев: {comments_count}')