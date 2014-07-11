from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone

#from .forms import PostForm
from .models import MainPost, MainPostForm, ReplyPost, ReplyPostForm
# Create your views here.


class IndexView(ListView): 
    model = MainPost
    template_name = "posts/index.html"
    context_object_name = "post_list"
    
class PostNew(FormView): 
    template_name = "posts/post_new.html"
    form_class = MainPostForm
    success_url = '/posts/'
    def form_valid(self, form):
        form.save()
        return super(PostNew, self).form_valid(form)
    # success_url = reverse("posts:post-detail",args=(post_id,))

    
class MainPostEdit(UpdateView): 
    model = MainPost
    fields = ['title', 'content','tags']
    template_name_suffix = '_edit'
#    def form_valid(self, form):
#        instance = form.save(commit=False)
#        instance.last_modified_date = timezone.now()
#        instance.save()
#        return super(PostEdit, self).form_valid(form)


class PostDetails(DetailView): 
    template_name = "posts/post_detail.html"
    model = MainPost
    context_object_name = "mainpost"
    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        #context['replypost_list'] = ReplyPost.objects.all()
        context['replypost_list'] = ReplyPost.objects.filter(root=context['mainpost'])
        return context
    #need to display everything in the same subject. 

   
class ReplyPostNew(CreateView):
    model = ReplyPost
    fields = ['content','root']
    template_name = 'posts/replypost_new.html'
    #will need to redirect to the main post; will implement later. 
    def get_success_url(self):
        return self.object.get_absolute_url()

class ReplyPostDelete(DeleteView):
    model = ReplyPost
    template_name = 'posts/replypost_delete.html'
    #success_url = reverse_lazy('posts:post-index')
    def get_success_url(self):
        return self.object.get_absolute_url()