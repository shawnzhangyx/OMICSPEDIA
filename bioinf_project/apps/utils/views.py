from django.shortcuts import render, render_to_response
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.template import RequestContext
import markdown
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Comment, Vote, Rate, Bookmark
from wiki.models import Page
from posts.models import MainPost, ReplyPost
from meta.models import Report
# Create your views here.

class CommentNew(CreateView):
    template_name = "utils/comment_new.html"
    model = Comment
    fields = ['content']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentNew, self).dispatch(*args, **kwargs)
   
    def form_valid(self, form):
        # can write a more compact function.

        if self.kwargs['comment_on'] == 'wiki':
            target = Page.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'posts':
            target = MainPost.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'replyposts':
            target = ReplyPost.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'reports':
            target = Report.objects.get(pk=self.kwargs['pk'])

        form.instance = Comment(content_object=target, content = self.request.POST['content'], author=self.request.user)
        return super(CommentNew, self).form_valid(form)

    def get_success_url(self):
        if self.kwargs['comment_on'] == "wiki":
            return reverse('wiki:wiki-detail',kwargs={'pk':self.kwargs['pk']})
        elif self.kwargs['comment_on'] == "posts":
            return reverse('posts:post-detail', kwargs={'pk':self.kwargs['pk']})
        elif self.kwargs['comment_on'] == "replyposts":
            return reverse('posts:post-detail', kwargs={'pk':ReplyPost.objects.get(pk=self.kwargs['pk']).mainpost.pk })
        elif self.kwargs['comment_on'] == 'reports':
            return reverse('meta:report-detail', kwargs={'pk':self.kwargs['pk']})
#def json_response(**kwargs):
#    data = dict()
#    data.update(**kwargs)
#    return HttpResponse(json.dumps(data))

@login_required
def vote(request):

    content_type_name = request.POST.get("ct")
    obj_id = int(request.POST.get("id"))
    vote_status = request.POST.get("vstat")
    content_app, content_model = content_type_name.split('.')
    content_type = ContentType.objects.get(app_label=content_app, model=content_model)
    voter = request.user
    obj = content_type.get_object_for_this_type(pk=obj_id)
    # the author of the voted object will gain or lose reputation depending on the vote.
    if hasattr(obj, "author"):
        if voter == obj.author: 
            message = "You cannot vote for yourself." 
            return HttpResponse(json.dumps({"yourvote":0, "allvote": obj.get_vote_count(),"message":message}))
        
    try: vote = Vote.objects.get(content_type__pk=content_type.id,
                               object_id=obj_id, voter=voter)
    # if has not voted before, vote
    except Vote.DoesNotExist:
        # if clicked on "vote-up-off", vote up
        if vote_status.startswith("vote-up"):
            vote = Vote(content_type=content_type, object_id=obj_id, voter=voter, choice=1)
            vote.save()

        # if clicked on "vote-down-off", vote down
        elif vote_status.startswith("vote-down"):
            vote = Vote(content_type=content_type, object_id=obj_id, voter=voter, choice=-1)
            vote.save()

        else:
            return HttpReponse("error")
        obj.vote_count = obj.get_vote_count()
        obj.save()
        return HttpResponse(json.dumps({"yourvote":vote.choice, "allvote":obj.get_vote_count(), }))
    # if has voted before.
    else:
        # if already voted, throw an error 
        yourvote= 0
        message = "You've already voted."
    return HttpResponse(json.dumps({"yourvote":0, "allvote": obj.get_vote_count(),"message":message}))

@login_required
def rate(request):
    title =request.POST.get("title")
    rating = request.POST.get("rating")
    page = Page.objects.get(title=title)
    obj_type = ContentType.objects.get_for_model(page)
    obj_id = page.id
    try: rate = Rate.objects.get(content_type__pk=obj_type.id,
                               object_id=page.id, rater=request.user)
    except Rate.DoesNotExist:
        rate = Rate(content_type=obj_type,
                               object_id=page.id, rater=request.user, rating=int(rating))
    else:
        rate.rating = rating
    rate.save()
    return HttpResponse("Rating "+rating+" is stored in database.")

@login_required
def bookmark(request):

    content_type_name = request.POST.get("ct")
    obj_id = int(request.POST.get("id"))
    bookmark_status = request.POST.get("bstat")
    content_app, content_model = content_type_name.split('.')
    content_type = ContentType.objects.get(app_label=content_app, model=content_model)
    reader = request.user
    obj = content_type.get_object_for_this_type(pk=obj_id)
    # the author of the voted object will gain or lose reputation depending on the bookmark.
        
    try: bookmark = Bookmark.objects.get(content_type__pk=content_type.id,
                               object_id=obj_id, reader=reader)
    # if has not voted before, vote
    except Bookmark.DoesNotExist:
        # if clicked on "vote-up-off", vote up
        if bookmark_status.endswith("off"):
            bookmark = Bookmark(content_type=content_type, object_id=obj_id, reader=reader)
            bookmark.save()
        else:
            return HttpResponse("error")
        obj.bookmark_count +=1
        obj.save()
        return HttpResponse(json.dumps({"bookmark_count":obj.bookmark_count}))
    # if has voted before.
    else:
        bookmark.delete()
        obj.bookmark_count -= 1
        obj.save()
        return HttpResponse(json.dumps({"bookmark_count":obj.bookmark_count}))


def preview_markdown(request):
    context = RequestContext(request)
    if request.method=="GET":
        content = request.GET['content']
        mkd_content = markdown.markdown(content,
        extensions=['extra',
                    'wikilinks(base_url=/wiki/, end_url=/)',
                    'toc'],
        safe_mode='escape')
    return render_to_response('utils/preview_markdown.html', {'mkd_content': mkd_content}, context)


