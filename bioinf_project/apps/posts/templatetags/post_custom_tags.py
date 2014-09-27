from django import template
from django.http import HttpResponse
#from posts.models import MainPost
register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("posts/templatetags/post-tab.html")
def show_post_tab(post):
    return {'post': post}
    

@register.inclusion_tag("posts/templatetags/post-body.html")
def display_post_body(post, user, post_type):
    if post_type == "is_question":
        is_question = True
    else: 
        is_question = False
    return {'post':post, 'user':user,'is_question':is_question}        

