from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView

from .models import UserProfile
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

class UserListView(ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = "user_profile_list"
    
