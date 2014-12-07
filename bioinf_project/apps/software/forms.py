from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML, Column
from django.core.exceptions import ValidationError

from .models import Tool
from wiki.models import Page
#from tags.models import Tag

class ToolForm(forms.ModelForm):
    name = forms.CharField(required=True)
    page = forms.ModelChoiceField(label="page", queryset=Page.objects.all())
    # select tags that are software. 
    image = forms.ImageField(required=False)
    url = forms.URLField(required=False)
    language = forms.CharField(required=False)
    OS = forms.CharField(required=False)
    citation = forms.CharField(required=False)
    author_name = forms.CharField(required=False)
    author_affiliation = forms.CharField(required=False)
    author_contacts = forms.CharField(required=False)
    first_release_date = forms.DateField(required=False)
    latest_release_date = forms.DateField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "software-form"
        self.helper.layout = Layout(
            HTML('<h3> Software and description</h3>'),
            Div('name', css_class="col-sm-6"),
            Div('url', css_class="col-sm-6"),
            Div('image', css_class="col-sm-6"),
  #          HTML('<h3 class="clearfix"> Environment</h3>'),
            Div('language', css_class="col-sm-6"),
            Div('OS', css_class="col-sm-6"),
            Div('citation', css_class="col-sm-6"),
            Div('author_name', css_class="col-sm-6"),
            Div('author_affiliation', css_class="col-sm-6"),
            Div('author_contacts', css_class="col-sm-6"),
            Div('first_release_date', css_class="col-sm-6"),
            Div('latest_release_date', css_class="col-sm-6"),
            Div('page', css_class="col-sm-6"),

            ButtonHolder(
                Submit('submit', 'Save')
            )
        )

    class Meta:
        model = Tool
        #fields = ('name','page')
        

        
class ToolNewForm(forms.ModelForm):
    name = forms.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(ToolNewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "software-form"
        self.helper.layout = Layout(
            HTML('<h3> Software name</h3>'),
            Div('name', css_class="col-sm-12"),

            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = Tool
        fields = ('name',)