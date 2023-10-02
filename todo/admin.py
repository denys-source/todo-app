from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin

from todo.models import Project, Task, User, UserInfoTag


@register(User)
class CustomUserAdmin(UserAdmin):
    pass


@register(UserInfoTag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Task)
admin.site.register(Project)
