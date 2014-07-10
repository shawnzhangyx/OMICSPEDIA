from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
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

    
#class PostEdit(UpdateView): 
#    model = Post
#    fields = ['title', 'content','tags']
#    template_name_suffix = '_edit'
#    def form_valid(self, form):
#        instance = form.save(commit=False)
#        instance.last_modified_date = timezone.now()
#        instance.save()
#        return super(PostEdit, self).form_valid(form)


class PostDetails(DetailView): 
    template_name = "posts/post_detail.html"
    model = MainPost
    #need to display everything in the same subject. 
