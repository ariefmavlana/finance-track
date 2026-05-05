from django import template
from django.utils.formats import number_format

register = template.Library()


@register.filter
def currency(value, currency_code="IDR"):
    """Format angka sebagai currency. Contoh: {{ amount|currency:'IDR' }}"""
    try:
        value = float(value)
        formatted = number_format(value, decimal_pos=0, use_l10n=True)
        currency_symbols = {
            "IDR": "Rp",
            "USD": "$",
            "EUR": "€",
            "SGD": "S$",
            "JPY": "¥",
        }
        symbol = currency_symbols.get(currency_code, currency_code)
        return f"{symbol} {formatted}"
    except (ValueError, TypeError):
        return value


@register.filter
def percentage(value, decimals=1):
    """Format sebagai persentase. Contoh: {{ ratio|percentage }}"""
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "0%"


@register.filter
def abs_value(value):
    """Nilai absolut."""
    try:
        return abs(value)
    except (ValueError, TypeError):
        return value


@register.simple_tag
def budget_progress_color(percentage):
    """Return DaisyUI progress color berdasarkan persentase."""
    if percentage >= 100:
        return "progress-error"
    elif percentage >= 80:
        return "progress-warning"
    elif percentage >= 50:
        return "progress-info"
    return "progress-success"