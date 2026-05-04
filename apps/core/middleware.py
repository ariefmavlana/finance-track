import zoneinfo
from django.utils import timezone


class TimezoneMiddleware:
    """Aktifkan timezone berdasarkan preference user."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_tz = getattr(request.user, "timezone", "UTC")
            try:
                tzinfo = zoneinfo.ZoneInfo(user_tz)
                timezone.activate(tzinfo)
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()
        return self.get_response(request)


_current_user_storage = {}


class CurrentUserMiddleware:
    """Simpan current user di thread-local storage untuk akses di signals/services."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import threading
        _current_user_storage[threading.get_ident()] = (
            request.user if request.user.is_authenticated else None
        )
        response = self.get_response(request)
        _current_user_storage.pop(threading.get_ident(), None)
        return response


def get_current_user():
    """Dapatkan user yang sedang login dari mana saja."""
    import threading
    return _current_user_storage.get(threading.get_ident())


class HtmxSecurityMiddleware:
    """Pastikan HTMX request berasal dari host yang sama."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "htmx", None):
            current_url = request.META.get("HTTP_HX_CURRENT_URL", "")
            if current_url:
                from django.conf import settings
                allowed = f"{request.scheme}://{request.get_host()}"
                if not current_url.startswith(allowed):
                    from django.http import HttpResponseForbidden
                    return HttpResponseForbidden("Invalid HTMX origin")
        return self.get_response(request)
