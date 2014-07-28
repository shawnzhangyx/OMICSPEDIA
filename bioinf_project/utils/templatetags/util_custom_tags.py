from django import template
from django.http import HttpResponse
register = template.Library()


# Show the vote number and provide 
# vote options for the object #wiki, tools, posts. 
@register.inclusion_tag("utils/templatetags/vote_widget.html")
def display_vote_widget(obj, user):
    return {'object': obj, "user": user}
    

