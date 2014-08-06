from django import template
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from utils.models import Vote

register = template.Library()

# Show the vote number and provide 
# vote options for the object #wiki, tools, posts. 
@register.inclusion_tag("utils/templatetags/vote_widget.html")
def display_vote_widget(obj, user):

    obj_type = ContentType.objects.get_for_model(obj)
    try: vote = Vote.objects.get(content_type__pk=obj_type.id, 
                               object_id=obj.id, voter=user)
    except (TypeError, Vote.DoesNotExist) as e: 
        vote_type = "none"
    else:
        if vote.choice == 1:
            vote_type = "up"
        elif vote.choice == -1:
            vote_type = "down"

    return {"object": obj, "obj_type": obj_type.app_label+'.'+obj_type.model, 
            "obj_id": obj.id, "user": user, "vote_type": vote_type}
    

