from django import template
from django.http import HttpResponse
from itertools import chain
from posts.models import MainPost
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
def display_question_body(post, user, perms, post_type):
    if post_type == "is_question":
        is_question = True
    else: 
        is_question = False
    return {'post':post, 'user':user, 'perms':perms,'is_question':is_question}        

@register.inclusion_tag("posts/templatetags/discussion-body.html")
def display_discussion_body(post, user, perms, post_type, reply_number):
    if post_type == "is_question":
        is_question = True
    else: 
        is_question = False
    return {'post':post, 'user':user, 'perms':perms, 'is_question':is_question, 'reply_number':reply_number}        
    
@register.inclusion_tag("posts/templatetags/blog-body.html")
def display_blog_body(post, user, perms):
    return {'post':post, 'user':user, 'perms':perms}   
    
@register.inclusion_tag("posts/templatetags/post-info.html")
def display_post_info(post):
    return {'post': post}
    
@register.inclusion_tag("posts/templatetags/related-posts.html")
def display_related_posts(post):
    related_posts = MainPost.objects.none()
    for tag in post.tags.all():
        posts = tag.posts.exclude(pk = post.pk)
        related_posts = related_posts | posts
        related_posts = related_posts.order_by('-vote_count')
    return {'related_posts': related_posts}