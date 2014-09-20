# forms.py
from django import forms
from django_select2 import AutoModelSelect2TagField
from django_select2 import widgets
from .models import MainPost
from tags.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder
#class TagField(AutoModelSelect2TagField):
#    queryset = Tag.objects
#    search_fields = ['name__icontains', ]

#    def get_model_field_values(self, value):
#        return {'name': value}

class TagField(AutoModelSelect2TagField):
    queryset = Tag.objects
    search_fields = ['name__icontains']
    def get_model_field_values(self, value):
        return {'name': value}


class MainPostForm(forms.ModelForm):
    title = forms.CharField()
    tags= TagField(forms.RadioSelect, help_text="please type your tags")
    content = forms.CharField(widget=forms.Textarea)
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
        self.base_fields['tags'].help_text = ''
        self.helper = FormHelper()
        self.helper.form_class = "post-form"
        self.helper.layout = Layout(
            Fieldset(
                'Post Form',
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
    

