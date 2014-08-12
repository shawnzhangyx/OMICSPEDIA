from django import template
from django.http import HttpResponse
#from posts.models import MainPost
register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("posts/templatetags/post-tab.html")
def show_post_tab(post):
    return {'post': post}
    

        

