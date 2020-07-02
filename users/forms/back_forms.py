from django import forms
from django.forms import ModelForm

from users.models import (User, Profile, )

class ProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('__all__')
