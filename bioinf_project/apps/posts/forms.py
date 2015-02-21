# forms.py
from django import forms
from .models import MainPost, ReplyPost
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML
from django.core.exceptions import ValidationError

def validate_title(text):
    #validate form input for title
    words = text.strip().split(' ')
    if len(words) < 4: 
        raise ValidationError("A minimum of four words is required.")
    
def validate_content(text):
    text = text.strip()
    if len(text) < 20: 
        raise ValidationError("A minimum of 20 characters are required.")  
    
class MainPostForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_title], help_text="Be specific with the title. A minimum of four words is required.")
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all(), required=False)
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=MainPost.TYPE_CHOICE, help_text="Choose the right type of posts.")
    content = forms.CharField(widget=forms.Textarea, validators=[validate_content])
    

    def __init__(self, *args, **kwargs):
        super(MainPostForm, self).__init__(*args, **kwargs)
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                ' Create new post',
                Field('type'),
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
                Div(css_id="content-string-count"),
            ),
            ButtonHolder(
                HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = MainPost
        fields = ('title','tags','type')



class MainPostRevisionForm(forms.ModelForm):

    title = forms.CharField(validators=[validate_title], help_text="Be specific with the title. A minimum of four words is required.")
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all(), required=False)
    content = forms.CharField(widget=forms.Textarea, validators=[validate_content])
    summary = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MainPostRevisionForm, self).__init__(*args, **kwargs)
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
                Div(css_id="content-string-count"),
                Field('summary', placeholder="Briefly explain your changes (fix spelling, gramma, added content...)"),
            ),
            ButtonHolder(
            HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )
        )
    class Meta:
        model = MainPost
        fields = ('title','tags')

class ReplyPostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, validators=[validate_content])
    def __init__(self, *args, **kwargs):
        super(ReplyPostForm, self).__init__(*args, **kwargs)
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                ' Create new reply',
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
                Div(css_id="content-string-count"),
            ),
            ButtonHolder(
                HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = ReplyPost
        fields = ()
        
class ReplyPostRevisionForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea, validators=[validate_content])
    summary = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ReplyPostRevisionForm, self).__init__(*args, **kwargs)
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                'Editing post',
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
                Div(css_id="content-string-count"),
                Field('summary'),
            ),
            ButtonHolder(
            HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )
        )
    class Meta:
        model = ReplyPost
        fields = ()
        
        
MainPostForm.base_fields['tags'].help_text = 'Please type your tags. Tags are important for users to quickly locate relevant contents'
MainPostRevisionForm.base_fields['tags'].help_text = 'Please type your tags. Tags are important for users to quickly locate relevant contents'