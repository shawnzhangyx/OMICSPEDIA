# forms.py
from django import forms
from .models import MainPost
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder


class MainPostForm(forms.ModelForm):
    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all())
    content = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(MainPostForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'].help_text = 'Please type your tags'
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
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
        model = MainPost
        fields = ('title','tags')



class MainPostRevisionForm(forms.ModelForm):

    title = forms.CharField()
    tags= forms.ModelMultipleChoiceField(label="Tags", queryset=Tag.objects.all())
    content = forms.CharField(widget=forms.Textarea)
    summary = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MainPostRevisionForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'].help_text = 'Please type your tags'
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('tags'),
                Field('content'),
                Field('summary'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )
    class Meta:
        model = MainPost
        fields = ('title','tags')
    

