from django import template


register = template.Library()


#list the tags according to their hierarchical structure. 

@register.inclusion_tag("tags/show_tags_children.html")
def show_tag_children(tag):
    tag_children_list = tag.children.all()
    return {'tag_list': tag_children_list}
    
    