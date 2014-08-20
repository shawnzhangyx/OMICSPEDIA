from django.shortcuts import render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from .models import Comment, Vote
from wiki.models import Page
from posts.models import MainPost, ReplyPost

import json 
# Create your views here.

class CommentNew(CreateView):
    template_name = "wiki/comment_new.html"
    model = Comment
    fields = ['content']
    def form_valid(self, form):
        # can write a more compact function. 

        if self.kwargs['comment_on'] == 'wiki':
            target = Page.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'posts':
            target = MainPost.objects.get(pk=self.kwargs['pk'])
        elif self.kwargs['comment_on'] == 'replyposts':
            target = ReplyPost.objects.get(pk=self.kwargs['pk'])

        form.instance = Comment(content_object=target, content = self.request.POST['content'], author=self.request.user)
        return super(CommentNew, self).form_valid(form)

    def get_success_url(self):
        if self.kwargs['comment_on'] == "wiki":
            return reverse('wiki:wiki-detail',kwargs={'pk':self.kwargs['pk']}) 
        elif self.kwargs['comment_on'] == "posts":
            return reverse('posts:post-detail', kwargs={'pk':self.kwargs['pk']})
        elif self.kwargs['comment_on'] == "replyposts":
            return reverse('posts:post-detail', kwargs={'pk':ReplyPost.objects.get(pk=self.kwargs['pk']).mainpost.pk })

#def json_response(**kwargs):
#    data = dict()
#    data.update(**kwargs)
#    return HttpResponse(json.dumps(data))

def vote(request): 


    content_type_name = request.POST.get("ct")
    obj_id = int(request.POST.get("id"))
    vote_status = request.POST.get("vstat")
 #   return HttpResponse(obj_id)
    content_app, content_model = content_type_name.split('.')
    content_type = ContentType.objects.get(app_label=content_app, model=content_model)
    voter = request.user
    obj = content_type.get_object_for_this_type(pk=obj_id)
    try: vote = Vote.objects.get(content_type__pk=content_type.id, 
                               object_id=obj_id, voter=voter)
    # if has not voted before, vote
    except Vote.DoesNotExist:
        # if clicked on "vote-up-off", vote up
        if vote_status == "vote-up-off": 
            vote = Vote(content_type=content_type, object_id=obj_id, voter=voter, choice=1)
            vote.save()
        # if clicked on "vote-down-off", vote down
        elif vote_status == "vote-down-off":
            vote = Vote(content_type=content_type, object_id=obj_id, voter=voter, choice=-1)
            vote.save()
        else:
            return HttpReponse("error")
        return HttpResponse(json.dumps({"yourvote":vote.choice, "allvote":obj.get_vote_count()}))
    # if has voted before. 
    else:
        # if change mind and want to vote the other way: 
        if vote_status.endswith('off'):
            vote.choice = vote.choice * (-1)
            vote.save()
            return HttpResponse(json.dumps({"yourvote":vote.choice, "allvote": obj.get_vote_count()}))
        # if want to recall the vote 
        elif vote_status.endswith('on'):
            vote.delete()
        return HttpResponse(json.dumps({"yourvote":0, "allvote": obj.get_vote_count()}))

