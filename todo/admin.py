from django.contrib import admin
from django.contrib.admin.decorators import register

from todo.models import Project, Task, User


@register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task)
admin.site.register(Project)
