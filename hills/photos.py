"""Per-request record of the photos already placed on the page, so no photo appears twice."""
from contextvars import ContextVar

_used = ContextVar("hills_used_photos", default=None)


def used():
    return _used.get()


def reset():
    _used.set(set())


class PagePhotosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = _used.set(set())
        try:
            return self.get_response(request)
        finally:
            _used.reset(token)
