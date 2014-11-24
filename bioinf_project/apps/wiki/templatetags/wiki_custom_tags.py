from django import template
from django.http import HttpResponse
from tags.models import Tag
register = template.Library()


#list the tags according to their hierarchical structure.

@register.filter
def add_edit(text):
    return

@register.inclusion_tag("wiki/templatetags/comment-dialog.html")
def show_comment_dialog(comment,user):
    return {'comment': comment,'user':user}

@register.inclusion_tag("wiki/templatetags/show-wiki-tab.html")
def show_wiki_tab(wiki):
    return {'wiki':wiki}

@register.inclusion_tag("wiki/templatetags/show-wiki-comment-warning.html")
def show_wiki_comment_warning(comment):
    return {'comment':comment}