from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.core.mixins import OwnershipMixin
from apps.finance.models import FinancialAccount


class AccountListView(LoginRequiredMixin, OwnershipMixin, ListView):
    model = FinancialAccount
    template_name = "finance/accounts/list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        return FinancialAccount.objects.filter(user=self.request.user, is_active=True)


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = FinancialAccount
    template_name = "finance/accounts/_form.html"
    success_url = reverse_lazy("finance:account-list")
    fields = ["name", "account_type", "currency", "initial_balance"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        account = form.save(commit=False)
        account.current_balance = account.initial_balance
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, OwnershipMixin, UpdateView):
    model = FinancialAccount
    template_name = "finance/accounts/_form.html"
    success_url = reverse_lazy("finance:account-list")
    fields = ["name", "account_type", "currency", "is_active"]

    def get_queryset(self):
        return FinancialAccount.objects.filter(user=self.request.user)


class AccountDetailView(LoginRequiredMixin, OwnershipMixin, DetailView):
    model = FinancialAccount
    template_name = "finance/accounts/detail.html"

    def get_queryset(self):
        return FinancialAccount.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["transactions"] = self.object.transactions.all()[:20]
        return ctx
