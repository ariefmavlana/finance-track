from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse, StreamingHttpResponse
from django.utils import timezone

from apps.core.mixins import HtmxMixin


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "finance/reports/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        start = today.replace(day=1)
        end = today
        
        ctx["report"] = {}
        ctx["start_date"] = start
        ctx["end_date"] = end
        return ctx


class ReportDataView(LoginRequiredMixin, HtmxMixin, TemplateView):
    """HTMX: load report data untuk range tertentu."""
    template_name = "finance/reports/_report_data.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        start_str = self.request.GET.get("start_date")
        end_str = self.request.GET.get("end_date")

        try:
            from datetime import datetime
            start = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else today.replace(day=1)
            end = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today
        except ValueError:
            start = today.replace(day=1)
            end = today

        ctx["report"] = {}
        ctx["start_date"] = start
        ctx["end_date"] = end
        return ctx


class ReportExportCsvView(LoginRequiredMixin, View):
    def get(self, request):
        from datetime import datetime
        
        start_str = request.GET.get("start_date")
        end_str = request.GET.get("end_date")

        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
            end = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
        except ValueError:
            start = end = None

        transactions = request.user.transactions.all()
        if start:
            transactions = transactions.filter(date__gte=start)
        if end:
            transactions = transactions.filter(date__lte=end)

        response = StreamingHttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"
        return response
