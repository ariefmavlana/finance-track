from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.core.mixins import OwnershipMixin
from apps.finance.models import Budget


class BudgetListView(LoginRequiredMixin, OwnershipMixin, ListView):
    model = Budget
    template_name = "finance/budgets/list.html"
    context_object_name = "budgets"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = "finance/budgets/_form.html"
    success_url = reverse_lazy("finance:budget-list")
    fields = ["name", "category", "amount", "currency", "period", "start_date"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, OwnershipMixin, UpdateView):
    model = Budget
    template_name = "finance/budgets/_form.html"
    success_url = reverse_lazy("finance:budget-list")
    fields = ["name", "category", "amount", "currency", "period", "start_date"]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetDeleteView(LoginRequiredMixin, OwnershipMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy("finance:budget-list")

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetRowView(LoginRequiredMixin, OwnershipMixin, DetailView):
    model = Budget
    template_name = "finance/budgets/_budget_row.html"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
