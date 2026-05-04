from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_TRANSFER = "transfer"

    CATEGORY_TYPES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
        (TYPE_TRANSFER, "Transfer"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="categories",
        null=True, blank=True,
    )
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    icon = models.CharField(max_length=50, default="tag")
    color = models.CharField(max_length=7, default="#6B7280")
    is_system = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
    )

    class Meta:
        db_table = "finance_category"
        verbose_name_plural = "categories"
        ordering = ["name"]
        unique_together = [("user", "name", "parent")]

    def __str__(self) -> str:
        return self.name