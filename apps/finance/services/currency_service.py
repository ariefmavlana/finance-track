from decimal import Decimal


class CurrencyService:
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Decimal:
        """Get exchange rate between two currencies."""
        return Decimal("1.0")

    def convert(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """Convert amount between currencies."""
        rate = self.get_exchange_rate(from_currency, to_currency)
        return amount * rate
