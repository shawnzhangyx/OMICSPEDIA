from django import template
from django.http import HttpResponse
#from posts.models import MainPost
register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("posts/templatetags/post-tab.html")
def show_post_tab(post):
    return {'post': post}

    
@register.inclusion_tag("posts/templatetags/post-tab-sm.html")
def show_post_tab_sm(post):
    return {'post':post}

@register.inclusion_tag("posts/templatetags/answer-tab-sm.html")
def show_answer_tab_sm(answer):
    return {'answer':answer}
    
@register.inclusion_tag("posts/templatetags/question-body.html")
def display_question_body(post, user, post_type):
    if post_type == "is_question":
        is_question = True
    else: 
        is_question = False
    return {'post':post, 'user':user,'is_question':is_question}        

@register.inclusion_tag("posts/templatetags/discussion-body.html")
def display_discussion_body(post, user, post_type, reply_number):
    if post_type == "is_question":
        is_question = True
    else: 
        is_question = False
    return {'post':post, 'user':user,'is_question':is_question, 'reply_number':reply_number}        
    
@register.inclusion_tag("posts/templatetags/blog-body.html")
def display_blog_body(post, user):
    return {'post':post, 'user':user}   