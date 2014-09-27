# forms.py

from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML
# Create your forms here.

class UserShortForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserShortForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('Username'),
                Field('Password'),
            ),
             ButtonHolder(
                Submit('submit', 'Log in'),
                HTML('''<a class="btn btn-primary" href="{% url 'users:register' %}">Register</a>'''),
            )

        )
    class Meta:
        model = User
        fields = ('username','password')

