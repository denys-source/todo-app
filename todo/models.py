from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from taggit.managers import TaggableManager


class User(AbstractUser):
    pass


class Project(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(default=timezone.now)
    project = models.ForeignKey(
        Project,
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.CASCADE
    )
    tags = TaggableManager()

    class Meta:
        ordering = (
            "completed",
            "due_date",
        )

    def __str__(self) -> str:
        return self.title
