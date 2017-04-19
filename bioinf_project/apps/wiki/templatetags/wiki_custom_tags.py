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
def show_wiki_comment_warning(comments):
    OTHER, GRAMMER, WIKILINK, EXPAND, CHECK_REFERENCE, ADD_REFERENCE, IMAGE, LEAD, NEW_INFO = range(9)
    dict = {OTHER: 'Therer is some comments about this page',
            GRAMMER: 'There is grammer error in this page',
            WIKILINK: 'Some wikilink may be not functional',
            EXPAND: 'This page is too short, please expand it',
            CHECK_REFERENCE: 'References may be inaccurate',
            ADD_REFERENCE: 'Rerefences are largely missing',
            IMAGE:'add some image',
            LEAD:'please improve the lead section of this page',
            NEW_INFO:'please provide some new information on this page'}
            
    issue_list = []
    warning_list = []
    for comment in comments:
        issue_list.append(comment.issue)
    issue_list = list(set(issue_list))
    for issue in issue_list:
        warning_list.append(dict[issue])
   
    return {'warnings':warning_list}
    
@register.inclusion_tag("wiki/templatetags/show-wiki-revision-tab.html")
def show_wiki_revision_tab(revision):
    return {'revision':revision}