from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class ReportService:
    def get_summary(self, user: User, start: date, end: date):
        """Get financial summary for date range."""
        return {
            "income": 0,
            "expense": 0,
            "net": 0,
        }
