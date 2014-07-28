from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone

#from .forms import PostForm
from .models import MainPost, ReplyPost, MainPostRevision, ReplyPostRevision
from .models import MainPostComment, ReplyPostComment
# Create your views here.


class IndexView(ListView): 
    model = MainPost
    template_name = "posts/index.html"
    context_object_name = "post_list"
    
class MainPostNew(CreateView): 
    template_name = "posts/post_new.html"
    model = MainPost
    fields = ['title', 'tags']
    
    def form_valid(self, form):
        form.save()
        new_revision = MainPostRevision(content=self.request.POST['content'], post=form.instance)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(MainPostNew, self).form_valid(form)

    

    
class MainPostEdit(UpdateView): 
    model = MainPost
    fields = ['title','tags']
    template_name = 'posts/mainpost_edit.html'
    
    def form_valid(self, form):
        new_revision = MainPostRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], post=self.object)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(MainPostEdit, self).form_valid(form)


class PostDetails(DetailView): 
    template_name = "posts/post_detail.html"
    model = MainPost
    context_object_name = "mainpost"
    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        context['replypost_list'] = ReplyPost.objects.filter(mainpost=context['mainpost'])
        return context
    #need to display everything in the same subject. 

   
class ReplyPostNew(CreateView):
    model = ReplyPost
    fields = []
    template_name = 'posts/replypost_new.html'
    #will need to redirect to the main post; will implement later. 
    def get_success_url(self):
        return self.object.get_absolute_url()
    def get_context_data(self, **kwargs):
        context = super(ReplyPostNew, self).get_context_data(**kwargs)
        context['mainpost'] = MainPost.objects.get(id=self.kwargs['mainpost_id'])
        return context

    def form_valid(self, form):
        form.instance.mainpost = MainPost.objects.get(pk = int(self.kwargs['mainpost_id']))
        form.save()
        new_revision = ReplyPostRevision(content=self.request.POST['content'], post=form.instance)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(ReplyPostNew, self).form_valid(form)
        
class ReplyPostEdit(UpdateView):
    model = ReplyPost
    fields = []
    template_name = 'posts/replypost_edit.html'

    def form_valid(self, form):
        new_revision = ReplyPostRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], post=self.object)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(ReplyPostEdit, self).form_valid(form)

class ReplyPostDelete(DeleteView):
    model = ReplyPost
    template_name = 'posts/replypost_delete.html'
    #success_url = reverse_lazy('posts:post-index')
    def get_success_url(self):
        return self.object.get_absolute_url()

