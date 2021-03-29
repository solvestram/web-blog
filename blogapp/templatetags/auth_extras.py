from django import template

register = template.Library()

@register.filter
def can_write_blogs(user):
    return user.groups.filter(name='can_write_blogs').exists()