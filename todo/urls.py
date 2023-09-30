from django.urls import path

from todo.views import RegisterView, TaskListView


urlpatterns = [
    # path("", HomePageView.as_view(), name="home"),
    path("task-list/", TaskListView.as_view(), name="task-list"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
]
