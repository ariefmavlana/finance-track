from django.contrib.auth.mixins import LoginRequiredMixin
from django_htmx.http import HttpResponseClientRedirect


class HtmxMixin:
    """
    Mixin untuk view yang merespons baik HTMX maupun regular request.
    Tentukan htmx_template untuk partial response.
    """
    htmx_template: str = ""
    full_template: str = ""

    def get_template_names(self):
        if getattr(self.request, "htmx", None) and self.htmx_template:
            return [self.htmx_template]
        if self.full_template:
            return [self.full_template]
        return super().get_template_names()

    def htmx_redirect(self, url: str):
        """Redirect yang benar di dalam HTMX request."""
        if getattr(self.request, "htmx", None):
            return HttpResponseClientRedirect(url)
        from django.shortcuts import redirect
        return redirect(url)


class OwnershipMixin:
    """Pastikan user hanya bisa akses object miliknya sendiri."""
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class FinanceViewMixin(LoginRequiredMixin, OwnershipMixin, HtmxMixin):
    """Base mixin untuk semua finance views."""
    pass


class HtmxOnlyMixin:
    """Tolak request yang bukan dari HTMX."""
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, "htmx", None):
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest("This endpoint is HTMX-only.")
        return super().dispatch(request, *args, **kwargs)
