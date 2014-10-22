# forms.py
from django import forms
from .models import Report
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder


class ReportForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "report-form"
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title'),
                Field('content'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = Report
        fields = ('title',)



