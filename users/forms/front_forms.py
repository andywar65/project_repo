from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from django.utils.translation import gettext as _

from captcha.fields import ReCaptchaField

from users.models import (Profile, User, UserMessage, )
from users.widgets import SmallClearableFileInput

class RegistrationForm(ModelForm):
    username = UsernameField(label = _('Username'), required = True,
        widget=forms.TextInput(attrs={'autofocus': True, }))
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label=_("I subscribe the privacy agreement"),
        required=True)
    if settings.RECAPTCHA_TEST_MODE == False:
        captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', )

class ContactLogForm(ModelForm):

    class Meta:
        model = UserMessage
        fields = ('user', 'email', 'subject', 'body', 'attachment', 'recipient')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': _("Write here the subject")}),
            'body': forms.Textarea(attrs={'placeholder': _("Write here the message")}),
            'attachment' : SmallClearableFileInput(),}

class ContactForm(ModelForm):
    nickname = forms.CharField(label = _('Name'), required = True,
        widget=forms.TextInput(attrs={'autofocus': True,}))
    email = forms.EmailField(label = _('Email'), required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label=_("I subscribe the privacy agreement"),
        required=True)

    captcha = ReCaptchaField()

    class Meta:
        model = UserMessage
        fields = ('nickname', 'email', 'subject', 'body', 'privacy')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': _("Write here the subject")}),
            'body': forms.Textarea(attrs={'placeholder': _("Write here the message")}),
            }

class FrontAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
        }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            }),
    )

class FrontPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, label=_('Signup email'),
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            })
    )

class FrontSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
        strip=False, label=_('New password'),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False, label=_('Repeat new password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
    )

class FrontPasswordChangeForm(FrontSetPasswordForm):
    old_password = forms.CharField(
        strip=False, label=_('Old password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'autofocus': True, }),
    )

class ProfileChangeForm(forms.Form):
    avatar = forms.FileField( required = False, widget = SmallClearableFileInput())
    first_name = forms.CharField( label = _('First name'), required = True,
        widget = forms.TextInput())
    last_name = forms.CharField( label = _('Last name'), required = True,
        widget = forms.TextInput())
    email = forms.EmailField(label = _('Email'), required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = _('Short bio'), required = False,
        widget = forms.Textarea(attrs={'placeholder': _("Talk about yourself")}) )
    yes_spam = forms.BooleanField( label=_("Mailing list"), required = False,
        help_text = _("Want to receive notifications about new articles?"))
    city_name = forms.CharField( label = _('City name'), required = False,
        widget = forms.TextInput())
    lat = forms.FloatField( label = _('Latitude'), required = False,
        help_text = _('Click on map to select'))
    long = forms.FloatField( label = _('Longitude'), required = False,)
    zoom = forms.FloatField( label = _('Zoom factor'), required = False,
        help_text = _('Zoom on map to set'))

class ProfileDeleteForm(forms.Form):
    delete = forms.BooleanField( label=_("Delete the profile"), required = True,
        help_text = _("Check to delete the profile."))
