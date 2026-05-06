from django.db.models.signals import post_save
from django.dispatch import receiver
from task_manager.models import Task
from account.models import User

@receiver(post_save, sender=Task)
def create_task_created_comment(sender, instance, created, **kwargs):
    """Сигнал: при создании задачи автоматически добавляем комментарий"""
    if created:
        user = User.objects.first()
        if user:
            from task_manager.models import Comment
            Comment.objects.create(
                task=instance,
                author=user,
                text=f"Task created: {instance.title}"
            )
            print(f"Сигнал: Создан комментарий для задачи {instance.title}")