# forms.py
from django import forms

from .models import Page
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML


class PageForm(forms.ModelForm):
    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all())
    content = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'].help_text = 'Please type your tags'
        self.helper = FormHelper()
        self.helper.form_class = "page-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('tags'),
                Field('content'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = Page
        fields = ('title','tags')



class PageRevisionForm(forms.ModelForm):

    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all(),required=False)
    content = forms.CharField(widget=forms.Textarea)
    summary = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(PageRevisionForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'].help_text = 'Please type your tags'
        self.helper = FormHelper()
        # self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('tags'),
                Field('content'),
                Field('summary'),
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
    

