from django.db import models
from account.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class ProjectDetail(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='details'
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    repository_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'project_details'
        verbose_name = 'Project detail'
        verbose_name_plural = 'Project details'

    def __str__(self):
        return f'Details: {self.project.name}'