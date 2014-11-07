from django import template
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from utils import diff_match_patch

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

#@register.inclusion_tag("utils/templatetags/text_diff.html")
@register.simple_tag
def show_text_diff(text1,text2):
        func = diff_match_patch.diff_match_patch()
        diff = func.diff_main(text1, text2)
        func.diff_cleanupSemantic(diff)
        htmldiff = func.diff_prettyHtml(diff)
        return htmldiff


## need to troubleshoot this 
@register.filter
def age(value):
    now = datetime.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
