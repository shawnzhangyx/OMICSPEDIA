from django import forms


class PostForm(forms.Form): 
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)
    tag = forms.CharField(max_length=255)