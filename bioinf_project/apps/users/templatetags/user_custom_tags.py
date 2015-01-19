from django import template
from django.http import HttpResponse
from tags.models import Tag
register = template.Library()


#list the tags according to their hierarchical structure.

@register.inclusion_tag("users/templatetags/display_user_md.html")
def display_user_md(user, field):
    return {'user_profile': user, 'field': field}
    
    
@register.inclusion_tag("users/templatetags/display_user_xs.html")
def display_user_xs(user):
    return {'user': user}