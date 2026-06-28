import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule
import json


def setup_periodic_tasks():
    print("Настройка периодических задач...")

    # Задача 1: Каждые 3 минуты 40 секунд (220 секунд)
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=220,
        period=IntervalSchedule.SECONDS,
    )
    task1, _ = PeriodicTask.objects.get_or_create(
        interval=interval,
        name='Task every 3 min 40 sec',
        task='task_manager.tasks.task_every_3_minutes_40_seconds',
        defaults={'enabled': True, 'one_off': False}
    )
    print(f"✅ Задача 1: {task1.name}")

    # Задача 2: 3 раза с 19 по 21 число, каждый час
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=0,
        hour='*',
        day_of_month='19,20,21',
        month_of_year='*',
        day_of_week='*',
    )
    task2, _ = PeriodicTask.objects.get_or_create(
        crontab=crontab_schedule,
        name='Task run on 19-21 every hour',
        task='task_manager.tasks.task_run_3_times',
        defaults={'enabled': True, 'one_off': False}
    )
    print(f"✅ Задача 2: {task2.name}")

    # Задача 3: Восход солнца
    solar_schedule, _ = SolarSchedule.objects.get_or_create(
        event='sunrise',
        latitude=55.7558,
        longitude=37.6173,
    )
    task3, _ = PeriodicTask.objects.get_or_create(
        solar=solar_schedule,
        name='Sunrise notification',
        task='task_manager.tasks.send_sunrise_notification',
        defaults={'enabled': True, 'one_off': False}
    )
    print(f"✅ Задача 3: {task3.name}")

    print("\nВсе периодические задачи настроены!")


if __name__ == '__main__':
    setup_periodic_tasks()