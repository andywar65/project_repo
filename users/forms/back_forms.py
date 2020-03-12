from django import forms
#from django.contrib.auth import (password_validation, )
#from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    #PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
#from captcha.fields import ReCaptchaField
from users.models import (User, Profile, )#Applicant, UserMessage
#from .choices import *

class ProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('__all__')
