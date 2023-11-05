from collections.abc import Callable
from threading import current_thread
from typing import TYPE_CHECKING, Union

from django.http import HttpRequest, HttpResponse

if TYPE_CHECKING:
    from todo.models import User


_requests = {}


def get_current_user() -> Union["User", None]:
    request = _requests.get(current_thread().ident, None)
    if request:
        return request.user
    return None


class CurrentRequestUserMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        _requests[current_thread().ident] = request

        response = self.get_response(request)

        _requests.pop(current_thread().ident, None)
        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        _requests.pop(current_thread().ident, None)
