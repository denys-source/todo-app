from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo.urls", namespace="todo")),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
    ),
    path("accounts/", include("django.contrib.auth.urls")),
] + (
    [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    if settings.DEBUG
    else []
)
