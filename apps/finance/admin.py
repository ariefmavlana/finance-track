from django.contrib import admin
from .models import FinancialAccount, Category, Transaction, Tag, Budget, RecurringTransaction


@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "account_type", "currency", "current_balance", "is_active"]
    list_filter = ["account_type", "currency", "is_active"]
    search_fields = ["name", "user__email"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_type", "user", "is_system", "parent"]
    list_filter = ["category_type", "is_system"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "amount", "currency", "transaction_type", "date", "status"]
    list_filter = ["transaction_type", "status", "currency"]
    search_fields = ["description", "payee", "user__email"]
    date_hierarchy = "date"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "color"]
    search_fields = ["name"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "category", "amount", "currency", "period", "is_active"]
    list_filter = ["period", "is_active"]
    search_fields = ["name", "user__email"]


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "amount", "frequency", "next_due_date", "is_active"]
    list_filter = ["frequency", "is_active"]
    search_fields = ["description"]