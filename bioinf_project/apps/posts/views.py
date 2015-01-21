from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# models 
from .models import MainPost, ReplyPost, MainPostRevision, ReplyPostRevision
from .models import MainPostComment, ReplyPostComment
# forms
from .forms import MainPostForm, MainPostRevisionForm, ReplyPostForm, ReplyPostRevisionForm
# to mask the manytomany field message. 

# Create your views here.


class IndexView(ListView):
    model = MainPost
    template_name = "posts/index.html"
    context_object_name = "post_list"
    paginate_by = 20
    
    def get_queryset(self):
        tab = self.request.GET.get('tab')
        sort = self.request.GET.get('sort')
        dict = {'Votes':'-vote_count','Replies':'-reply_count', 'Bookmarks':'bookmark_count','Views':'view_count'}
        if sort in dict:
            sort_by = dict[sort]
        else: 
            sort_by = '-vote_count'
        if tab =="Question":
            return MainPost.questions.order_by(sort_by)
        elif tab =="Unanswered":
            return MainPost.questions.filter(reply_count=0).order_by(sort_by)
        elif tab =="Discussion":
            return MainPost.discussions.order_by(sort_by)
        elif tab =="Blog":
            return MainPost.blogs.order_by(sort_by)
        else: 
            return MainPost.objects.all().order_by(sort_by)
            
    def get_context_data(self,**kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab')
        context['sort'] = self.request.GET.get('sort')
        context['question_count'] = MainPost.questions.count()
        context['discussion_count'] = MainPost.discussions.count()
        context['blog_count'] = MainPost.blogs.count()
        context['unanswered_count'] = MainPost.questions.filter(reply_count=0).count()
        return context

class MainPostNew(CreateView):
    template_name = "posts/post_new.html"
    form_class = MainPostForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainPostNew, self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        new_revision = MainPostRevision(content=self.request.POST['content'], post=form.instance,
                author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(MainPostNew, self).form_valid(form)




class MainPostEdit(UpdateView):
    form_class = MainPostRevisionForm
    template_name = 'posts/post_new.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainPostEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return MainPost.objects.get(pk=self.kwargs['pk'])

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)

    def form_valid(self, form):
        new_revision = MainPostRevision(content=self.request.POST['content'],
                       revision_summary=self.request.POST['summary'], post=self.object,
                       author=self.request.user)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(MainPostEdit, self).form_valid(form)


class PostDetails(DetailView):
    #template_name = "posts/post_detail.html"
    model = MainPost
    context_object_name = "mainpost"

    def get_template_names(self):
        if self.object.type == 0:
            return  ['posts/question_detail.html']
        elif self.object.type == 1:
            return  ['posts/discussion_detail.html']
        elif self.object.type == 2:
            return  ['posts/blog_detail.html']
        else: 
            return  ['posts/post_detail.html']
    def get_object(self):
        obj = super(PostDetails, self).get_object()
        MainPost.update_post_views(obj, request=self.request)
        return obj
    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
        if not tab:
            if self.object.get_type_display() == "question":
                tab = 'votes'
            else: 
                tab = "oldest"
        sort_dict = {'votes':'-vote_count','oldest':'created'}
        sort_value = sort_dict[tab]
        replies = ReplyPost.objects.filter(mainpost=context['mainpost']).order_by(sort_value)
        context['replypost_list'] = replies
        context['tab'] = tab
        context['type'] = self.object.get_type_display
        context['comments'] = context['mainpost'].get_comments().order_by(sort_value)
        return context
    #need to display everything in the same subject.


class ReplyPostNew(CreateView):
    template_name = "posts/post_new.html"
    form_class = ReplyPostForm
    #will need to redirect to the main post; will implement later.
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReplyPostNew, self).dispatch(*args, **kwargs)
        
    def get_success_url(self):
        return self.object.get_absolute_url()
        
    def get_context_data(self, **kwargs):
        context = super(ReplyPostNew, self).get_context_data(**kwargs)
        context['mainpost'] = MainPost.objects.get(id=self.kwargs['mainpost_id'])
        return context

    def form_valid(self, form):
        form.instance.mainpost = MainPost.objects.get(pk = int(self.kwargs['mainpost_id']))
        form.instance.author = self.request.user
        form.save()
        new_revision = ReplyPostRevision(content=self.request.POST['content'], post=form.instance, 
                        author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(ReplyPostNew, self).form_valid(form)

class ReplyPostEdit(UpdateView):
    template_name = "posts/post_new.html"
    form_class = ReplyPostRevisionForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReplyPostEdit, self).dispatch(*args, **kwargs)

    def get_object(self):
        return ReplyPost.objects.get(pk=self.kwargs['pk'])

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)
        
    def form_valid(self, form):
        new_revision = ReplyPostRevision(content=self.request.POST['content'], 
                       revision_summary=self.request.POST['summary'], post=self.object, 
                       author=self.request.user)
        new_revision.save()
        self.object.current_revision=new_revision
        self.object.save()
        return super(ReplyPostEdit, self).form_valid(form)

class ReplyPostDelete(DeleteView):
    model = ReplyPost
    template_name = 'posts/replypost_delete.html'
    #success_url = reverse_lazy('posts:post-index')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReplyPostDelete, self).dispatch(*args, **kwargs)
        
    def get_success_url(self):
        return self.object.get_absolute_url()

class ReplyPostAccept(UpdateView):
    model = ReplyPost
    fields = []
    template_name = 'posts/replypost_accept.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReplyPostAccept, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return ReplyPost.objects.get(pk=self.kwargs['pk'])
        
    def form_valid(self, form):
        self.object.mainpost.accepted_answer=self.object
        self.object.mainpost.save()
        return super(ReplyPostAccept, self).form_valid(form)
    def get_success_url(self):
        return self.object.get_absolute_url()
        
class MainPostHistory(ListView):
    model = MainPostRevision
    template_name = "posts/post_revision_history.html"
    context_object_name = "revision_list"

    def get_queryset(self):
        return MainPostRevision.objects.filter(post__id = self.kwargs['pk']).order_by('-modified_date')

class ReplyPostHistory(ListView):
    model = ReplyPostRevision
    template_name = "posts/post_revision_history.html"
    context_object_name = "revision_list"

    def get_queryset(self):
        return ReplyPostRevision.objects.filter(post__id = self.kwargs['pk']).order_by('-modified_date')


