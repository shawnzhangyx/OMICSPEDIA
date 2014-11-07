# forms.py
from django import forms
from .models import MainPost
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML


class MainPostForm(forms.ModelForm):
    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    

    def __init__(self, *args, **kwargs):
        super(MainPostForm, self).__init__(*args, **kwargs)
        #self.base_fields['tags'].help_text = 'Please type your tags'
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                ' Create new post',
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
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



class MainPostRevisionForm(forms.ModelForm):

    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    summary = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MainPostRevisionForm, self).__init__(*args, **kwargs)
        #self.base_fields['tags'].help_text = 'Please type your tags'
        self.fields['content'].label=""
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                'Editing post',
                Field('title'),
                Field('tags'),
                HTML('''<div id="wmd-button-bar"></div> '''),
                Field('content', id="wmd-input"),
                Field('summary'),
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
    

