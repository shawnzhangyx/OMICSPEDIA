from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from .forms import PostForm
from .models import Post
# Create your views here.


class IndexView(ListView): 
    model = Post
    templte_name = "post/index.html"
    
class PostNew(FormView): 
    template_name = "post/post_new.html"
    form_class = PostForm
    post_id = 1 # test
    success_url = reverse("posts:post-detail",args=(post_id,))
    
class PostDetails(DetailView): 
    template_name = "post/post_detail.html"
    model = Post
    #need to display everything in the same subject. 