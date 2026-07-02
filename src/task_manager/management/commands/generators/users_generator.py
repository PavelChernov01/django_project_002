from faker import Faker
from account.models import User

fake = Faker('ru_RU')


def generate_users(self, stdout, count):
    """Создание пользователей"""
    stdout.write('\n2. Создание пользователей...')
    users = []
    for i in range(count):
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
            stdout.write(f'   Создано пользователей: {i + 1}')

    stdout.write(f'   Создано пользователей: {len(users)}')
    return users