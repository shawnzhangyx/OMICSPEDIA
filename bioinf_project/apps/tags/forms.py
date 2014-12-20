from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML, Column
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import Tag
from wiki.models import Page

def validate_icon(image):
    w, h = get_image_dimensions(image)
    if w != 24 and h != 24: 
        raise ValidationError("the uploaded icon must be 24by24.")

def validate_name(name):
    if name.find("_") >= 0:
        raise ValidationError("'_' is not allowed in the tag name")

class TagCreateForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name],help_text="the name of the tag")
    icon = forms.ImageField(label="Icon", required=False, validators=[validate_icon], help_text="24px * 24px")
    categories = forms.ChoiceField(choices=Tag.CATEGORY_CHOICE, 
    help_text='select category')
    
    def __init__(self, *args, **kwargs):
        super(TagCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "tag-form"
        self.helper.layout = Layout(
            Div('name', css_class="col-sm-6"),
            Div('categories',css_class="col-sm-6"),
            Div('icon', css_class="col-sm-6"),
            Div('', css_class="clearfix visible-sm-block visible-md-block visible-lg-block"),
            ButtonHolder(
                Submit('submit', 'Submit'), css_class="col-sm-6"
            )
        )
        
    class Meta:
        model = Tag
        fields = ('name', 'categories','icon')
        
        
class TagForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name],help_text="the name of the tag")
    wiki_page = forms.ModelChoiceField(label="page", queryset=Page.objects.all(),help_text="the wiki page of this tag")
    icon = forms.ImageField(label="Icon", required=False, validators=[validate_icon], help_text="24px * 24px")
    categories = forms.ChoiceField(choices=Tag.CATEGORY_CHOICE, 
    help_text='select category')
    
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "tag-form"
        self.helper.layout = Layout(
            Div('name', css_class="col-sm-6"),
            Div('wiki_page',css_class="col-sm-6"),
            Div('categories',css_class="col-sm-6"),
            Div('icon', css_class="col-sm-6"),
            Div('', css_class="clearfix visible-sm-block visible-md-block visible-lg-block"),
            ButtonHolder(
                Submit('submit', 'Submit'), css_class="col-sm-6"
            )
        )
        
    class Meta:
        model = Tag
        fields = ('name', 'wiki_page', 'categories','icon')
        
        
class WorkflowTagForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name],help_text="the name of the tag")
    wiki_page = forms.ModelChoiceField(label="page", queryset=Page.objects.all(),help_text="the wiki page of this tag")
    parent = forms.ModelChoiceField(label="parent", queryset=Tag.objects.filter(categories__exact = 1), help_text='Choose a parent node', required=False)
    icon = forms.ImageField(label="Icon", required=False, validators=[validate_icon], help_text="24px * 24px")
    categories = forms.ChoiceField(choices=Tag.CATEGORY_CHOICE, 
    help_text='select category')
    
    def __init__(self, *args, **kwargs):
        super(WorkflowTagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "tag-form"
        self.helper.layout = Layout(
            Div('name', css_class="col-sm-6"),
            Div('wiki_page',css_class="col-sm-6"),
            Div('parent', css_class="col-sm-6"),
            Div('categories',css_class="col-sm-6"),
            Div('icon', css_class="col-sm-6"),
            Div('', css_class="clearfix visible-sm-block visible-md-block visible-lg-block"),
            ButtonHolder(
                Submit('submit', 'Submit'), css_class="col-sm-6"
            )
        )
        
    class Meta:
        model = Tag
        fields = ('name', 'wiki_page', 'categories','icon', 'parent')