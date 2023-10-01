from django.urls import path

from todo.views import (
    ProjectListView,
    RegisterView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    update_completed,
)


urlpatterns = [
    # path("", HomePageView.as_view(), name="home"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "tasks/<int:pk>/detail/", TaskDetailView.as_view(), name="task-detail"
    ),
    path(
        "tasks/<int:pk>/update-completed/",
        update_completed,
        name="task-update-completed",
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
]

app_name = "todo"
