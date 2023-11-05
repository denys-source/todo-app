from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin

from todo.models import Project, Tag, Task, User


@register(User)
class CustomUserAdmin(UserAdmin):
    pass


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Task)
admin.site.register(Project)
