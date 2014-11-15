from django import template
from django.http import HttpResponse
from tags.models import Tag
register = template.Library()


#list the tags according to their hierarchical structure.

@register.inclusion_tag("tags/templatetags/show_tags_children.html")
def show_tag_children(tag):
    tag_children_list = tag.children.all()
    return {'tag_list': tag_children_list}


@register.inclusion_tag("tags/templatetags/show_omics_tag_children.html")
def show_omics_tag_children(tag):
    tag_children_list = tag.children.all()
    return {'tag_list': tag_children_list}


@register.inclusion_tag("tags/templatetags/show_tag_ancestor.html")
def show_tag_ancestor(tag):
     try:
        tag.parent
     # if there is no parent to this tag.
     except AttributeError:
        return
     return {'tag': tag.parent}
#    else:

@register.inclusion_tag("tags/templatetags/display_tag_list.html")
def display_tag_list(tag_list):
    return {'tag_list': tag_list}

@register.inclusion_tag("tags/templatetags/display_tag_user_contribution.html")
def display_tag_user_contribution(tags, user, list_num):
    num_answers = []
    for tag in tags:
        answers = user.replypost_set.filter(mainpost__tags = tag)
        tag.num_answers = answers.count()
        num_answers.append(answers.count())
    # sort the tags by the num of answers
    tags = sorted(tags, key=lambda x:-x.num_answers)[0:list_num]
    num_answers = sorted(num_answers, key=lambda x: -x)[0:list_num]
    return {'zipped': zip(tags, num_answers),'list_num': list_num}
    
    