from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def htmx_or_full(context, htmx_template, full_template):
    """
    Pilih template berdasarkan apakah request adalah HTMX.
    Penggunaan: {% htmx_or_full 'partial.html' 'full.html' %}
    """
    request = context.get("request")
    if request and getattr(request, "htmx", None):
        return htmx_template
    return full_template