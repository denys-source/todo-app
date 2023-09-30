from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from todo.forms import RegisterForm
from todo.models import Task


class TaskListView(ListView):
    model = Task


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
