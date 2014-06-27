from django import forms

from .models import Post

class PostForm(forms.Form): 
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)
    tag = forms.CharField(max_length=255)
#    def fill_form(self): 
