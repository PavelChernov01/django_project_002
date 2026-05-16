from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from task_manager.models import Task, Attachment
from account.models import User
import os


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


@receiver(post_delete, sender=Attachment)
def delete_attachment_file(sender, instance, **kwargs):
    """Удаляет файл с диска при удалении объекта Attachment"""
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
                print(f"Файл удалён: {instance.file.path}")
        except Exception as e:
            print(f"Ошибка удаления файла: {e}")