from datetime import timedelta
from datetime import datetime
from typing import Any

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.urls import reverse, reverse_lazy
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
from django.utils import timezone

from todo.forms import (
    FilterForm,
    ProjectForm,
    ProjectSearchForm,
    RegisterForm,
    TaskForm,
    TaskSearchForm,
)
from todo.models import Project, Task


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["common_tags"] = Task.tags.most_common()[:5]

        search_form = TaskSearchForm(
            initial={"q": self.request.GET.get("q", "")}
        )
        context["search_form"] = search_form

        filter_form = FilterForm()
        for param, value in self.request.GET.items():
            if param != "date":
                filter_form.fields[param] = forms.CharField(
                    widget=forms.HiddenInput(attrs={"value": value})
                )
        context["filter_form"] = filter_form

        context["today"] = str(timezone.now().date())
        context["tomorrow"] = str((timezone.now() + timedelta(days=1)).date())

        return context

    def get_queryset(self) -> QuerySet[Task]:
        queryset = Task.objects.filter(user=self.request.user)

        if date_string := self.request.GET.get("date"):
            try:
                date_obj = datetime.strptime(date_string, "%Y-%m-%d")
                queryset = queryset.filter(due_date=date_obj)
            except ValueError:
                pass

        if tag_list := self.request.GET.getlist("tag"):
            queryset = queryset.filter(tags__name__in=tag_list)

        if query := self.request.GET.get("q"):
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form: TaskForm) -> HttpResponse:
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
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
        return redirect(request.META.get("HTTP_REFERER", ""))
    return redirect(request.META.get("HTTP_REFERER", ""))


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_form = ProjectSearchForm(
            initial={"q": self.request.GET.get("q", "")}
        )
        context["search_form"] = search_form
        return context

    def get_queryset(self) -> QuerySet[Project]:
        queryset = Project.objects.filter(user=self.request.user)
        if query := self.request.GET.get("q"):
            queryset = queryset.filter(name__icontains=query)
        return queryset


class ProjectDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset = self.object.tasks.all()
        if tag_list := self.request.GET.getlist("tag"):
            queryset = queryset.filter(tags__name__in=tag_list)
        context["task_list"] = queryset
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("todo:project-list")

    def form_valid(self, form: ProjectForm) -> HttpResponse:
        project = form.save(commit=False)
        project.user = self.request.user
        project.save()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self) -> str:
        return reverse("todo:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Project
    template_name = "todo/project_delete.html"
    success_url = reverse_lazy("todo:project-list")


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
