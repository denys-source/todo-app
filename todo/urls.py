from django.urls import path

from todo.views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    RegisterView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    tag_delete_view,
    toggle_completed_status,
    home_page_view,
)


urlpatterns = [
    path("", home_page_view, name="home"),
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
        toggle_completed_status,
        name="task-update-completed",
    ),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/detail/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path("tags/<int:pk>/delete/", tag_delete_view, name="tag-delete"),
]

app_name = "todo"
