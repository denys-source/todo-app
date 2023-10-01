from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin

from todo.models import Project, Task, User


@register(User)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(Task)
admin.site.register(Project)
