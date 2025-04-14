from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def format_action_type(value):
    """Formats action_type by replacing underscores with spaces and capitalizing words"""
    if not value:
        return "System Activity"
    return value.replace('_', ' ').title()
