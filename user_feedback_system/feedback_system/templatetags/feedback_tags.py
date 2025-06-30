from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css):
    """
    Add a CSS class to a form field
    Usage: {{ form.field|addclass:'form-control' }}
    """
    return field.as_widget(attrs={"class": css})

@register.simple_tag
def is_staff_user(user):
    """
    Check if user is staff
    Usage: {% is_staff_user user as is_staff %}
    """
    return user.is_staff