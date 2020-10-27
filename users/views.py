from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from .forms import (RegistrationForm, ContactForm,
    ContactLogForm, FrontAuthenticationForm, FrontPasswordResetForm,
    FrontSetPasswordForm, FrontPasswordChangeForm, ProfileChangeForm,
    ProfileDeleteForm)
from .models import User, Profile

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

def registration_message( username, password ):
    #TODO have some info in settings
    message = f"""
        Ciao {username}! \n
        Abbiamo ricevuto la tua registrazione al sito {settings.WEBSITE_NAME}.\n
        Puoi effettuare il Login al seguente link: \n
        {settings.BASE_URL}/accounts/login/ \n
        Usa il nome utente da te scelto: {username}
        e questa password: {password} (possibilmente da cambiare).
        Una volta effettuato il login potrai gestire il tuo profilo.
        Grazie.
        Lo staff di {settings.WEBSITE_NAME} \n
        Link utili:
        Informativa sulla privacy: {settings.BASE_URL}/docs/privacy/
        Cambio password: {settings.BASE_URL}/accounts/password_change/
        """
    return message

class RegistrationFormView(GetMixin, FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = '/registration?submitted=True'

    def form_valid(self, form):
        user = form.save(commit=False)
        password = User.objects.make_random_password()
        user.password = make_password(password)
        user.save()
        subject = f'Credenziali di accesso a {settings.WEBSITE_ACRO}'
        body = registration_message(user.username, password)
        mailto = [ user.email, ]
        email = EmailMessage(subject, body, settings.SERVER_EMAIL, mailto)
        email.send()
        return super(RegistrationFormView, self).form_valid(form)

class ContactFormView(GetMixin, FormView):
    form_class = ContactForm
    template_name = 'users/message.html'
    success_url = '/contacts?submitted=True'

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        if 'subject' in self.request.GET:
            initial.update({'subject': self.request.GET['subject']})
        return initial

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return ContactLogForm
        return super(ContactFormView, self).get_form_class()

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'users/message_log.html'
        return super(ContactFormView, self).get_template_names()

    def form_valid(self, form):
        message = form.save(commit=False)
        if self.request.user.is_authenticated:
            message.user = self.request.user
            message.email = self.request.user.email
            if 'recipient' in self.request.GET:
                try:
                    recip = User.objects.get(id=self.request.GET['recipient'])
                    message.recipient = recip.email
                except:
                    pass
        message.save()
        if not message.recipient:
            message.recipient = settings.DEFAULT_RECIPIENT
        subject = message.subject
        msg = (message.body + '\n\nDa: '+ message.get_full_name() +
            ' (' + message.get_email() + ')')
        mailto = [message.recipient, ]
        email = EmailMessage(subject, msg, settings.SERVER_EMAIL,
            mailto)
        if message.attachment:
            email.attach_file(message.attachment.path)
        email.send()
        return super(ContactFormView, self).form_valid(form)

class FrontLoginView(LoginView):
    template_name = 'users/front_login.html'
    form_class = FrontAuthenticationForm

    def get_redirect_url(self):
        """Avoid going from login to logout and other ambiguous situations"""
        redirect_to = super(FrontLoginView, self).get_redirect_url()
        if redirect_to == reverse('front_logout'):
            return reverse('profile')
        elif redirect_to == reverse('password_reset_done'):
            return reverse('profile')
        elif redirect_to == reverse('profile_deleted'):
            return reverse('profile')
        elif redirect_to == reverse('registration'):
            return reverse('profile')
        return redirect_to

class FrontLogoutView(LogoutView):
    template_name = 'users/front_logout.html'

class FrontPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = FrontPasswordResetForm

class TemplateResetView(TemplateView):
    template_name = 'users/reset_password_done.html'

class FrontPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_password_confirm.html'
    form_class = FrontSetPasswordForm

class TemplateResetDoneView(TemplateView):
    template_name = 'users/reset_done.html'

class TemplateAccountView(LoginRequiredMixin, GetMixin, TemplateView):
    template_name = 'users/account.html'

class FrontPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = FrontPasswordChangeForm

class FrontPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'users/profile_change.html'

    def get(self, request, *args, **kwargs):
        if request.user.uuid != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()
        initial.update({'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'avatar': self.request.user.profile.avatar,
            'bio': self.request.user.profile.bio,
            'yes_spam': self.request.user.profile.yes_spam,
            })
        return initial

    def form_valid(self, form):
        user = User.objects.get(id = self.request.user.uuid )
        profile = Profile.objects.get(pk = user.uuid)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        profile.avatar = form.cleaned_data['avatar']
        profile.bio = form.cleaned_data['bio']
        profile.yes_spam = form.cleaned_data['yes_spam']
        user.save()
        profile.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get_success_url(self):
        return f'/accounts/profile/?submitted={self.request.user.get_full_name()}'

class ProfileDeleteView(LoginRequiredMixin, FormView):
    form_class = ProfileDeleteForm
    template_name = 'users/profile_delete.html'
    success_url = '/accounts/profile/deleted'

    def get(self, request, *args, **kwargs):
        if request.user.uuid != kwargs['pk']:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileDeleteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(id = self.request.user.uuid )
        user.is_active = False
        user.first_name = ''
        user.last_name = ''
        user.email = ''
        user.save()
        profile = Profile.objects.get(pk = user.uuid)
        profile.delete()
        return super(ProfileDeleteView, self).form_valid(form)

class TemplateDeletedView(TemplateView):
    template_name = 'users/profile_deleted.html'
