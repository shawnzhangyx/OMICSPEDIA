from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML, Column
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import Tag
from wiki.models import Page

def validate_icon(image):
    w, h = get_image_dimensions(image)
    if (float(w)/h < 0.95 or float(w)/h >1.05): 
        raise ValidationError("Please make sure the height and width are approximately same (5 percent difference), otherwise the image will be distorted. Your image: width: %d; height: %d"% (w,h))
        
def validate_name(name):
    if name.find("_") >= 0:
        raise ValidationError("'_' is not allowed in the tag name")



class TagCreateForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name],help_text="the name of the tag")
    categories = forms.ChoiceField(choices=Tag.CATEGORY_CHOICE, 
    help_text='select category')
    
    def __init__(self, *args, **kwargs):
        super(TagCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "tag-form"
        self.helper.layout = Layout(
            Div('name', css_class="col-sm-6"),
            Div('categories',css_class="col-sm-6"),
    #        Div('icon', css_class="col-sm-6"),
            Div('', css_class="clearfix visible-sm-block visible-md-block visible-lg-block"),
            ButtonHolder(
                Submit('submit', 'Submit'), css_class="col-sm-6"
            )
        )
        
    class Meta:
        model = Tag
        fields = ('name', 'categories',)
             
class TagForm(forms.ModelForm):
    name = forms.CharField(validators=[validate_name],help_text="the name of the tag")
    wiki_page = forms.ModelChoiceField(label="page", queryset=Page.objects.all(),help_text="the wiki page of this tag")
    icon = forms.ImageField(label="Icon", required=False, validators=[validate_icon], help_text="Upload image with same height and width.")
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
    icon = forms.ImageField(label="Icon", required=False, validators=[validate_icon], help_text="50px * 50px")
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
    def clean(self):
        cleaned_data = super(WorkflowTagForm, self).clean()
        categories = cleaned_data.get('categories')
        parent = cleaned_data.get('parent')
        if categories !='1' and parent: 
            cleaned_data['parent'] = None
            self._errors['parent'] = self.error_class(['Non-workflow tag cannot have a parent'])     
        return cleaned_data
        
    class Meta:
        model = Tag
        fields = ('name', 'wiki_page', 'categories','icon', 'parent')