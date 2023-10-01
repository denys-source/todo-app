from django.urls import path

from todo.views import (
    RegisterView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    update_completed,
)


urlpatterns = [
    # path("", HomePageView.as_view(), name="home"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/detail/", TaskDetailView.as_view(), name="task-detail"
    ),
    path(
        "tasks/<int:pk>/update-completed/",
        update_completed,
        name="task-update-completed",
    ),
]

app_name = "todo"