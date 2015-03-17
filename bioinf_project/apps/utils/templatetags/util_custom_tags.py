from django import template
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from utils import diff_match_patch
from django.utils import timezone

from utils.models import Vote, Bookmark, ImageAttachment, View
from wiki.models import PageRevision
from posts.models import MainPost, ReplyPost, MainPostRevision, ReplyPostRevision
register = template.Library()

# Show the vote number and provide
# vote options for the object #wiki, tools, posts.
@register.inclusion_tag("utils/templatetags/vote_widget.html")
def display_vote_widget(obj, user):

    obj_type = ContentType.objects.get_for_model(obj)
    try: vote = Vote.objects.get(content_type__pk=obj_type.id,
                               object_id=obj.id, voter=user)
    except (TypeError, Vote.DoesNotExist) as e:
        if user.is_authenticated():
            message="you can vote" 
            vote_type= "open"
            if hasattr(obj, 'author'):
                if user == obj.author: 
                    vote_type= "block"
                    message = "You cannot vote yourself."
                elif user.exceed_vote_limit():
                    vote_type="block"
                    message = "You've reached daily vote limit"
        else: 
            vote_type="block"
            message = "please log in to vote."
    else:
        message = "you've already voted."
        if vote.choice == 1:
            vote_type = "up"
        elif vote.choice == -1:
            vote_type = "down"

    return {"object": obj, "obj_type": obj_type.app_label+'.'+obj_type.model, 
            "obj_id": obj.id, "user": user, "vote_type": vote_type, "message":message}

@register.inclusion_tag("utils/templatetags/vote_up_widget.html")
def display_vote_up(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    try: vote = Vote.objects.get(content_type__pk=obj_type.id,
                               object_id=obj.id, voter=user)
    except (TypeError, Vote.DoesNotExist) as e:
        if user.is_authenticated():
            message="you can vote"
            vote_type= "open"
            if hasattr(obj, 'author'):
                if user == obj.author: 
                    vote_type= "block"
                    message = "You cannot vote yourself."
                elif user.exceed_vote_limit():
                    vote_type="block"
                    message = "You've reached daily vote limit"
        else: 
            vote_type="block"
            message = "please log in to vote."
    else:
        message = "you've already voted."
        vote_type = "up"
    return {"object": obj, "obj_type": obj_type.app_label+'.'+obj_type.model, 
            "obj_id": obj.id, "user": user, "vote_type": vote_type, "message":message}
            
@register.inclusion_tag("utils/templatetags/bookmark_widget.html")
def display_bookmark_widget(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    try: bookmark = Bookmark.objects.get(content_type__pk=obj_type.id,
                               object_id=obj.id, reader=user)
    except (TypeError, Bookmark.DoesNotExist) as e:
        marked = "no"
    else:
        marked = "yes"
    return {"object": obj, "obj_type": obj_type.app_label+'.'+obj_type.model, 
            "obj_id": obj.id, "user": user, "marked": marked}
                        
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

@register.inclusion_tag("utils/templatetags/image_widget.html")
def display_image_widget(obj, user, path):
    obj_type = ContentType.objects.get_for_model(obj)
    images = ImageAttachment.objects.filter(content_type__pk=obj_type.id,
            object_id=obj.id)
           
    return {"images":images, "user":user, "type_id":obj_type.id, "obj_id":obj.id, "path":path}
    
    
@register.simple_tag
def get_sitewide_stats():
    time = timezone.now()- timedelta(hours=24)
    # views and visits
    views = View.objects.filter(date__gte = time)
    view_count = views.count()
    unique_ip = views.values('ip').distinct().count()
    # edits 
    edits = PageRevision.objects.filter(modified_date__gte = time).count() \
            + MainPostRevision.objects.filter(modified_date__gte = time).count() \
            + ReplyPostRevision.objects.filter(modified_date__gte = time).count()
    ## generate the string
    string = '<ul class="list-unstyled">'
    
    string += '<li><b>'+str(view_count)+ '</b> page view'
    if view_count > 1:
        string += 's'
    string += ' </li><li><b>' + str(edits) +'</b> edit'
    if edits > 1:
        string +='s'
    string +=' </li><li><b>'+ str(unique_ip) + '</b> visitor'
    if unique_ip > 1:
        string += 's'
    string += ' </li></ul>'
    return string
    
    
    