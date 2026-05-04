from django.conf import settings


def global_context(request):
    """Context processor: tersedia di semua template."""
    ctx = {
        "debug": settings.DEBUG,
        "base_currency": settings.FINTRACK_BASE_CURRENCY,
        "supported_currencies": settings.FINTRACK_SUPPORTED_CURRENCIES,
    }
    if request.user.is_authenticated:
        ctx["user_timezone"] = request.user.timezone
    return ctx