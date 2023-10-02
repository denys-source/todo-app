from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase, slugify
from crum import get_current_user


class User(AbstractUser):
    pass


class UserInfoTag(TagBase):
    user = models.ForeignKey(
        User, related_name="tags", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        self.user = user
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class TaggedTask(GenericTaggedItemBase):
    tag = models.ForeignKey(
        UserInfoTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


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
    tags = TaggableManager(blank=True, through=TaggedTask)

    class Meta:
        ordering = (
            "completed",
            "due_date",
        )

    def __str__(self) -> str:
        return self.title
