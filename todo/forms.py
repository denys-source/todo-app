from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm

from todo.models import Project, Task, User


class RegisterForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-input"

    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-input"

    class Meta:
        model = Task
        fields = ("title", "description", "due_date", "project", "tags")
        widgets = {"due_date": forms.widgets.DateInput(attrs={"type": "date"})}


class TaskSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Search task"}
        ),
    )


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-input"

    class Meta:
        model = Project
        fields = ("name",)


class FilterForm(forms.Form):
    pass
