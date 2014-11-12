from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView
from django.contrib.contenttypes.models import ContentType

from .models import UserProfile
from posts.models import MainPost
from wiki.models import Page
from software.models import Tool
from .forms import UserCreationForm, ProfileForm
# Create your views here.

####  account related views ####
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    success_url = '/'

class Login(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.request.GET['next'])

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
   
   
   
####  profile related views  ####
class ProfileEdit(UpdateView):
    form_class=ProfileForm
    template_name = "users/profile_edit.html"
    def get_object(self):
        return UserProfile.objects.get(pk=self.kwargs['pk'])
        
        
class ProfileView(DetailView):
    model = UserProfile
    template_name = "users/profile_view.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        bookmarks = self.object.user.bookmarks.all()
        # bookmarked posts
        post_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(MainPost))
        id = post_bookmarks.values_list('object_id',flat=True)
        bookmark_posts = MainPost.objects.filter(id__in = id)
        context['bookmark_posts'] = bookmark_posts
        # bookmarked wiki
        wiki_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(Page))
        id = wiki_bookmarks.values_list('object_id',flat=True)
        bookmark_wiki = Page.objects.filter(id__in = id)
        context['bookmark_wiki'] = bookmark_wiki
        # bookmarked software
        software_bookmarks = bookmarks.filter(content_type=ContentType.objects.get_for_model(Tool))
        id = software_bookmarks.values_list('object_id',flat=True)
        bookmark_software = Tool.objects.filter(id__in = id)
        context['bookmark_software'] = bookmark_software
        return context
        
class UserListView(ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = "user_profile_list"
    
