# forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Page, PageComment
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML


def validate_title(name):
    invalidChars = '!"#$%&\'()*+-/:;<=>?@[\\]^_`{|}~'
    for char in name:
        if char in invalidChars:
            raise ValidationError("special character " + char + " is not allowed in the wiki title")
        
        
class PageForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_title],help_text='title of the wiki. Special characters such as !"#$%&\'()*+-/:;<=>?@[\\]^_`{|}~ are not allowed')
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all(), required=False)
    content = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        #self.base_fields['tags'].help_text = 'Please type your tags'
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "page-form"
        self.helper.layout = Layout(
            Fieldset(
                'Create new wiki',
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content',id="wmd-input"),
            ),
            ButtonHolder(
                HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = Page
        fields = ('title','tags')

PageForm.base_fields['tags'].help_text = 'Please type your tags'

class PageRevisionForm(forms.ModelForm):

    title = forms.CharField(validators=[validate_title],help_text='title of the wiki. Special characters such as !"#$%&\'()*+-/:;<=>?@[\\]^_`{|}~ are not allowed')
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all(),required=False)
    content = forms.CharField(widget=forms.Textarea)
    summary = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(PageRevisionForm, self).__init__(*args, **kwargs)
        #self.base_fields['tags'].help_text = 'Please type your tags'
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "page-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content',id="wmd-input"),
                Field('summary', placeholder="Briefly explain your changes (fix spelling, gramma, added content...)"),
            ),
             ButtonHolder(
                HTML('''<span class="btn btn-primary" data-toggle="modal" 
                    data-target="#preview-mkd-text" id="preview-click">Preview</span>&nbsp&nbsp'''),
                Submit('submit', 'Submit')
            )

        )
    class Meta:
        model = Page
        fields = ('title','tags')
    
PageRevisionForm.base_fields['tags'].help_text = 'Please type your tags'

class PageCommentForm(forms.ModelForm):
    status = forms.ChoiceField(choices = PageComment.STATUS_CHOICE[0:2])
    issue = forms.ChoiceField(choices = PageComment.ISSUE_CHOICE)
    detail = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(PageCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "page-comment-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div('status', css_class="col-xs-8 col-sm-4"),
                Div('issue', css_class="col-xs-8 col-sm-4"),
                Div('detail', css_class="col-xs-12"),
            ),
             ButtonHolder(
                Submit('submit', 'Submit')
            )

        )
    class Meta:
        model = PageComment
        fields = ('status','issue', 'detail')