# forms.py

from django import forms
from .models import User, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, ButtonHolder, HTML
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Create your forms here.

def validate_email(email):
    try: user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        pass # this is great
    else:
        raise ValidationError( user.email+" has been already been registered.")

    
        
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(label="Email Address", validators=[validate_email])
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('',
                Field('email'),
                Field('password1'),
                Field('password2'),

            ),
            ButtonHolder(
                Submit('submit', 'Register')
            )
        )
        
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = User.objects.normalize_email(user.email)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        #    user_profile = UserProfile.objects.get_or_create(user=user)
        #    user_profile[0].save()
        return user

        
def validate_portrait(image):
    w, h = get_image_dimensions(image)
    if w > 400 or h > 400: 
        raise ValidationError("the uploaded image must be smaller than 400px in width or height. Your image: width: %d; height: %d"% (w,h))
    elif (float(w)/h < 0.95 or float(w)/h >1.05): 
        raise ValidationError("Please make sure the height and width are approximately same (5 percent difference), otherwise the image will be distorted. Your image: width: %d; height: %d"% (w,h))
        
class ProfileForm(forms.ModelForm):
    name = forms.CharField(required=False)
    location = forms.CharField(required=False)
    website = forms.URLField(required=False)
    biography = forms.CharField(widget=forms.Textarea, required=False)
    portrait = forms.ImageField(required=False, validators=[validate_portrait], help_text="400px*400px")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "profile-form"
        self.helper.layout = Layout(
            Fieldset(
                'Edit your profile',
                Field('name'),
                Field('location'),
                Field('website'),
                Field('biography'),
                Field('portrait'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )
    class Meta: 
        model = UserProfile
        fields = ['name', 'location','website', 'biography', 'portrait',]


