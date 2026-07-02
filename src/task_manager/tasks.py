from celery import shared_task
from celery.schedules import crontab
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
import time
import random


# ============================================
# ЗАДАЧА 3: Фоновые задачи
# ============================================

@shared_task
def add_numbers(x, y):
    """Простая задача сложения двух чисел"""
    result = x + y
    print(f"Сумма {x} + {y} = {result}")
    return result


@shared_task
def send_welcome_email(user_id):
    """Отправка приветственного письма пользователю"""
    try:
        user = User.objects.get(id=user_id)
        subject = 'Добро пожаловать!'
        message = f'Привет, {user.username}! Спасибо за регистрацию.'
        send_mail(subject, message, 'from@example.com', [user.email])
        print(f"Письмо отправлено пользователю {user.email}")
        return f"Email sent to {user.email}"
    except User.DoesNotExist:
        return "User not found"


@shared_task
def long_running_task():
    """Долгая задача (имитация)"""
    print("Запуск долгой задачи...")
    time.sleep(10)
    print("Долгая задача завершена")
    return "Task completed"


# ============================================
# ЗАДАЧА 4: Задачи по расписанию
# ============================================

@shared_task
def task_every_3_minutes_40_seconds():
    """Задача, выполняемая каждые 3 минуты 40 секунд"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Задача выполнена в {current_time}")
    return f"Task executed at {current_time}"


@shared_task
def task_run_3_times():
    """Задача, выполняемая 3 раза с 19 по 21 число, каждый час"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Задача выполнена в {current_time}")
    return f"Scheduled task at {current_time}"


# ============================================
# ЗАДАЧА 5: Solar задача (восход солнца)
# ============================================

@shared_task
def send_sunrise_notification():
    """Отправка уведомления на восходе солнца"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"☀️ Восход солнца! Время: {current_time}")
    print("🌅 Уведомление о восходе отправлено всем пользователям")
    return f"Sunrise notification sent at {current_time}"


@shared_task
def print_hello():
    """Простая задача для проверки"""
    print(f"Hello from Celery at {datetime.now()}")
    return "Hello!"