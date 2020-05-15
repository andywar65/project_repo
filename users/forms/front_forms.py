from datetime import datetime
from django import forms
from django.conf import settings
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from captcha.fields import ReCaptchaField
from users.models import (Profile, User, UserMessage, )#User,
from users.widgets import SmallClearableFileInput

class RegistrationForm(ModelForm):
    username = UsernameField(label = 'Nome utente', required = True,
        widget=forms.TextInput(attrs={'autofocus': True, }))
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label="Ho letto l'informativa sulla privacy",
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
            'subject': forms.TextInput(attrs={'placeholder': "Scrivi qui il soggetto"}),
            'body': forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}),
            'attachment' : SmallClearableFileInput(),}

class ContactForm(ModelForm):
    nickname = forms.CharField(label = 'Nome', required = True,
        widget=forms.TextInput(attrs={'autofocus': True,}))
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    privacy = forms.BooleanField(label="Ho letto l'informativa sulla privacy",
        required=True)

    captcha = ReCaptchaField()

    class Meta:
        model = UserMessage
        fields = ('nickname', 'email', 'subject', 'body', 'privacy')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': "Scrivi qui il soggetto"}),
            'body': forms.Textarea(attrs={'placeholder': "Scrivi qui il messaggio"}),
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
        max_length=254, label='Email di registrazione',
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            })
    )

class FrontSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
        strip=False, label='Nuova password',
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False, label='Ripeti la nuova password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
    )

class FrontPasswordChangeForm(FrontSetPasswordForm):
    old_password = forms.CharField(
        strip=False, label='Vecchia password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'autofocus': True, }),
    )

class ProfileChangeForm(forms.Form):
    avatar = forms.FileField( required = False, widget = SmallClearableFileInput())
    first_name = forms.CharField( label = 'Nome', required = True,
        widget = forms.TextInput())
    last_name = forms.CharField( label = 'Cognome', required = True,
        widget = forms.TextInput())
    email = forms.EmailField(label = 'Email', required = True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'placeholder': 'you@example.com'}))
    bio = forms.CharField( label = 'Breve biografia', required = False,
        widget = forms.Textarea(attrs={'placeholder': "Parlaci un po' di te"}) )
    yes_spam = forms.BooleanField( label="Mailing list", required = False,
        help_text = "Vuoi ricevere notifiche sui nuovi articoli?")

class ProfileDeleteForm(forms.Form):
    delete = forms.BooleanField( label="Cancella il profilo", required = True,
        help_text = """Seleziona per cancellare il profilo.""")
