from django import template
from django.http import HttpResponse
#from posts.models import MainPost
register = template.Library()


@register.inclusion_tag("software/templatetags/display_software_tab.html")
def display_software_tab(tool):
    return {'tool': tool}


@register.inclusion_tag("software/templatetags/display_software_tab_sm.html")
def display_software_tab_sm(tool):
    return {'tool': tool}