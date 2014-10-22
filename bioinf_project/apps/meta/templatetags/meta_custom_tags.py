from django import template
from django.http import HttpResponse
#from posts.models import MainPost
register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("meta/templatetags/report-tab.html")
def show_report_tab(report):
    return {'report': report}


@register.inclusion_tag("meta/templatetags/report-body.html")
def display_report_body(report, user):
       return {'report':report, 'user':user}

