from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView

from .models import UserProfile 
# Create your views here.

class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    def form_valid(self, form):
        new_user = form.instance
        new_user.save()
        new_user_profile = UserProfile(user=new_user)
        new_user_profile.save()
        return super(RegisterView,self).form_valid(form)
    success_url = '/'

class Login(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('index')

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
   

class ProfileView(DetailView):
    model = UserProfile
    template_name = "users/profile_view.html"

class UserListView(ListView):
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = "user_profile_list"
    