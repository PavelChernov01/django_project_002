import os
from django.db import models
from django.dispatch import receiver
from .task import Task


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    class Meta:
        db_table = 'attachments'
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename

    def is_image(self):
        """Проверяет, является ли файл изображением"""
        ext = os.path.splitext(self.file.name)[1].lower()
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']

@receiver(models.signals.post_delete, sender=Attachment)
def delete_file_on_delete(sender, instance, **kwargs):
    """Удаляет файл с диска при удалении объекта Attachment"""
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        except Exception:
            pass