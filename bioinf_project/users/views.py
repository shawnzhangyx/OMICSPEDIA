from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.views.generic.edit import FormView
# Create your views here.

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
    
