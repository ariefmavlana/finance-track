from django.urls import path
from apps.finance.views import dashboard, transactions, budgets, accounts, reports

app_name = "finance"

urlpatterns = [
    # ── Dashboard ─────────────────────────────────────────────
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("dashboard/summary/", dashboard.DashboardSummaryView.as_view(), name="dashboard-summary"),

    # ── Transactions ──────────────────────────────────────────
    path("transactions/", transactions.TransactionListView.as_view(), name="transaction-list"),
    path("transactions/create/", transactions.TransactionCreateView.as_view(), name="transaction-create"),
    path("transactions/<uuid:pk>/", transactions.TransactionDetailView.as_view(), name="transaction-detail"),
    path("transactions/<uuid:pk>/edit/", transactions.TransactionUpdateView.as_view(), name="transaction-update"),
    path("transactions/<uuid:pk>/delete/", transactions.TransactionDeleteView.as_view(), name="transaction-delete"),
    path("transactions/import/", transactions.TransactionImportView.as_view(), name="transaction-import"),
    path("transactions/export/", transactions.TransactionExportView.as_view(), name="transaction-export"),
    # HTMX-only partials
    path("transactions/filter/", transactions.TransactionFilterView.as_view(), name="transaction-filter"),
    path("transactions/<uuid:pk>/row/", transactions.TransactionRowView.as_view(), name="transaction-row"),

    # ── Budgets ───────────────────────────────────────────────
    path("budgets/", budgets.BudgetListView.as_view(), name="budget-list"),
    path("budgets/create/", budgets.BudgetCreateView.as_view(), name="budget-create"),
    path("budgets/<uuid:pk>/edit/", budgets.BudgetUpdateView.as_view(), name="budget-update"),
    path("budgets/<uuid:pk>/delete/", budgets.BudgetDeleteView.as_view(), name="budget-delete"),
    path("budgets/<uuid:pk>/row/", budgets.BudgetRowView.as_view(), name="budget-row"),

    # ── Accounts ──────────────────────────────────────────────
    path("accounts-list/", accounts.AccountListView.as_view(), name="account-list"),
    path("accounts/create/", accounts.AccountCreateView.as_view(), name="account-create"),
    path("accounts/<uuid:pk>/", accounts.AccountDetailView.as_view(), name="account-detail"),
    path("accounts/<uuid:pk>/edit/", accounts.AccountUpdateView.as_view(), name="account-update"),

    # ── Reports ───────────────────────────────────────────────
    path("reports/", reports.ReportView.as_view(), name="reports"),
    path("reports/data/", reports.ReportDataView.as_view(), name="reports-data"),
    path("reports/export/csv/", reports.ReportExportCsvView.as_view(), name="reports-export-csv"),
]
