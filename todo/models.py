from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser

from todo.middleware import get_current_user


class User(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    user = models.ForeignKey(
        User, related_name="tags", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name="projects", on_delete=models.CASCADE
    )

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
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = (
            "completed",
            "due_date",
        )

    def __str__(self) -> str:
        return self.title
