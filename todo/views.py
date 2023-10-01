from typing import Any
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from todo.forms import RegisterForm, TaskCreateForm
from todo.models import Task


class OwnerRequiredMixin:
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self) -> QuerySet[Task]:
        queryset = Task.objects.filter(user=self.request.user)
        return queryset


class TaskDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form: TaskCreateForm) -> HttpResponse:
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Task
    template_name = "todo/task_delete.html"
    success_url = reverse_lazy("todo:task-list")


@login_required
def update_completed(request, pk: int) -> HttpResponse:
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        if task.user != request.user:
            raise PermissionDenied()
        task.completed = not task.completed
        task.save()
        return redirect("todo:task-list")
    return redirect("todo:task-list")


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("todo:task-list")
    redirect_authenticated_user = True

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)
