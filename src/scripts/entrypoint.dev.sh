
set -e

# Применяем миграции базы данных
python src/manage.py migrate

# Запускаем сервер разработки
python src/manage.py runserver