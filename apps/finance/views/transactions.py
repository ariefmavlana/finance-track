from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_htmx.http import trigger_client_event

from apps.core.mixins import OwnershipMixin, HtmxMixin
from apps.finance.models import Transaction


class TransactionListView(LoginRequiredMixin, OwnershipMixin, ListView):
    model = Transaction
    template_name = "finance/transactions/list.html"
    context_object_name = "transactions"
    paginate_by = 25

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "finance/transactions/_form.html"
    success_url = reverse_lazy("finance:transaction-list")
    fields = ["account", "category", "transaction_type", "amount", "date", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionDetailView(LoginRequiredMixin, OwnershipMixin, DetailView):
    model = Transaction
    template_name = "finance/transactions/detail.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionUpdateView(LoginRequiredMixin, OwnershipMixin, UpdateView):
    model = Transaction
    template_name = "finance/transactions/_form.html"
    success_url = reverse_lazy("finance:transaction-list")
    fields = ["account", "category", "transaction_type", "amount", "date", "description"]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, OwnershipMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy("finance:transaction-list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionImportView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse("Import form")

    def post(self, request):
        return HttpResponseRedirect(reverse_lazy("finance:transaction-list"))


class TransactionExportView(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse("Export CSV")


class TransactionFilterView(LoginRequiredMixin, HtmxMixin, ListView):
    model = Transaction
    template_name = "finance/transactions/_list_partial.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionRowView(LoginRequiredMixin, OwnershipMixin, DetailView):
    model = Transaction
    template_name = "finance/transactions/_row.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
