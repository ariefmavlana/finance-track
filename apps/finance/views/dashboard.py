from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from apps.core.mixins import HtmxMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "finance/dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localtime()
        
        ctx["today"] = today
        ctx["summary"] = {}
        ctx["recent_transactions"] = []
        ctx["budgets"] = []
        return ctx


class DashboardSummaryView(LoginRequiredMixin, HtmxMixin, TemplateView):
    """HTMX polling endpoint untuk KPI cards."""
    template_name = "finance/dashboard/_kpi_cards.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localtime()
        ctx["summary"] = {}
        ctx["today"] = today
        return ctx
