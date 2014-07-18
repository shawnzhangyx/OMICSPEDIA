from django import template
from django.http import HttpResponse

register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("tags/show_tags_children.html")
def show_tag_children(tag):
    tag_children_list = tag.children.all()
    return {'tag_list': tag_children_list}
    
@register.simple_tag
def show_tag_parent(tag):
    if tag.parent:
        return show_tag_parent(tag.parent)+ ' / ' + tag.name
    else:
        return tag.name

@register.inclusion_tag("tags/show_tag_ancestor.html")
def show_tag_ancestor(tag):
#    tag_parent = tag.parent
#    if tag.parent:
        return {'tag': tag.parent}
#    else: 
        

